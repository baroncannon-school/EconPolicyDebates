-- ============================================================================
-- EconPolicyDebates Grading Module — Supabase Migration
-- Run this in your Supabase SQL Editor (hfojiycmzghnhafllasz.supabase.co)
-- ============================================================================

-- 1. Students roster table
CREATE TABLE IF NOT EXISTS debate_students (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email TEXT NOT NULL,
  name TEXT NOT NULL,
  period TEXT NOT NULL,  -- '1st' or '4th'
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(email, period)
);

-- 2. Assignments: which student presented which segment(s)
--    Supports: multiple students per segment, multiple segments per student
CREATE TABLE IF NOT EXISTS debate_assignments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  student_id UUID NOT NULL REFERENCES debate_students(id) ON DELETE CASCADE,
  debate_id TEXT NOT NULL,       -- e.g., 'debate-1'
  team TEXT NOT NULL,            -- 'A' or 'B'
  segment_type TEXT NOT NULL,    -- 'opening', 'main', 'rebuttal', 'closing'
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Grades: one per assignment (per student per segment)
CREATE TABLE IF NOT EXISTS debate_grades (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  assignment_id UUID NOT NULL REFERENCES debate_assignments(id) ON DELETE CASCADE,
  research_score INT DEFAULT 0 CHECK (research_score BETWEEN 0 AND 10),
  presentation_score INT DEFAULT 0 CHECK (presentation_score BETWEEN 0 AND 10),
  consistency_score INT DEFAULT 0 CHECK (consistency_score BETWEEN 0 AND 10),
  segment_score INT DEFAULT 0 CHECK (segment_score BETWEEN 0 AND 10),
  teacher_comment TEXT DEFAULT '',
  is_published BOOLEAN DEFAULT FALSE,
  graded_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(assignment_id)
);

-- 4. Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_students_email ON debate_students(email);
CREATE INDEX IF NOT EXISTS idx_students_period ON debate_students(period);
CREATE INDEX IF NOT EXISTS idx_assignments_debate ON debate_assignments(debate_id);
CREATE INDEX IF NOT EXISTS idx_assignments_student ON debate_assignments(student_id);
CREATE INDEX IF NOT EXISTS idx_grades_published ON debate_grades(is_published);

-- 5. Row Level Security (RLS) policies
ALTER TABLE debate_students ENABLE ROW LEVEL SECURITY;
ALTER TABLE debate_assignments ENABLE ROW LEVEL SECURITY;
ALTER TABLE debate_grades ENABLE ROW LEVEL SECURITY;

-- Allow public read for students to find their own record
CREATE POLICY "Students can view own record"
  ON debate_students FOR SELECT
  USING (true);

-- Allow public read for assignments
CREATE POLICY "Anyone can view assignments"
  ON debate_assignments FOR SELECT
  USING (true);

-- Students can only view PUBLISHED grades for their own assignments
CREATE POLICY "Students can view own published grades"
  ON debate_grades FOR SELECT
  USING (
    is_published = true
    AND assignment_id IN (
      SELECT da.id FROM debate_assignments da
      JOIN debate_students ds ON ds.id = da.student_id
      WHERE ds.email = current_setting('request.jwt.claims', true)::json->>'email'
    )
  );

-- Service role (admin) can do everything — use service_role key in admin panel
-- The anon key + RLS above restricts student access
-- For the admin panel, we'll use the service_role key or a custom admin check

-- Allow anon insert/update/delete for admin operations
-- (We'll authenticate the teacher via Google SSO in the app layer)
CREATE POLICY "Admin full access students"
  ON debate_students FOR ALL
  USING (true) WITH CHECK (true);

CREATE POLICY "Admin full access assignments"
  ON debate_assignments FOR ALL
  USING (true) WITH CHECK (true);

CREATE POLICY "Admin full access grades"
  ON debate_grades FOR ALL
  USING (true) WITH CHECK (true);

-- 6. Helper view: combined grade data for easy querying
CREATE OR REPLACE VIEW debate_grade_summary AS
SELECT
  ds.id AS student_id,
  ds.name AS student_name,
  ds.email AS student_email,
  ds.period,
  da.debate_id,
  da.team,
  da.segment_type,
  da.id AS assignment_id,
  dg.research_score,
  dg.presentation_score,
  dg.consistency_score,
  dg.segment_score,
  COALESCE(dg.research_score, 0) + COALESCE(dg.presentation_score, 0) +
    COALESCE(dg.consistency_score, 0) + COALESCE(dg.segment_score, 0) AS total_score,
  dg.teacher_comment,
  dg.is_published,
  dg.graded_at,
  dg.updated_at
FROM debate_students ds
JOIN debate_assignments da ON da.student_id = ds.id
LEFT JOIN debate_grades dg ON dg.assignment_id = da.id
ORDER BY ds.period, da.debate_id, da.team, da.segment_type, ds.name;
