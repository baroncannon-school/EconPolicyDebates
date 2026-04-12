import re

with open('/sessions/sleepy-confident-bell/mnt/outputs/debate-review.jsx', 'r') as f:
    jsx_code = f.read()

# Remove import lines
jsx_code = re.sub(r"^import React.*?from 'react';\n", '', jsx_code, flags=re.MULTILINE)
jsx_code = re.sub(r"^import \{[\s\S]*?\} from 'lucide-react';\n", '', jsx_code, flags=re.MULTILINE)
# Also remove any other import lines (e.g. separate lucide imports)
jsx_code = re.sub(r"^import \{[^}]*\} from 'lucide-react';\n?", '', jsx_code, flags=re.MULTILINE)

# Replace export default (now on the App wrapper)
jsx_code = jsx_code.replace('export default function App', 'function App')

# Inline SVG icon components
icons = '''
    const Icon = ({d, className = "w-4 h-4", fill = "none", stroke = "currentColor"}) => (
      <svg xmlns="http://www.w3.org/2000/svg" className={className} viewBox="0 0 24 24" fill={fill} stroke={stroke} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">{typeof d === 'string' ? <path d={d}/> : d}</svg>
    );
    const Play = ({className}) => <Icon className={className} d={<polygon points="5 3 19 12 5 21 5 3" fill="currentColor" stroke="none"/>}/>;
    const Pause = ({className}) => <Icon className={className} d={<><rect x="6" y="4" width="4" height="16" fill="currentColor" stroke="none"/><rect x="14" y="4" width="4" height="16" fill="currentColor" stroke="none"/></>}/>;
    const Search = ({className}) => <Icon className={className} d={<><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></>}/>;
    const ChevronLeft = ({className}) => <Icon className={className} d="M15 18l-6-6 6-6"/>;
    const ChevronRight = ({className}) => <Icon className={className} d="M9 18l6-6-6-6"/>;
    const Star = ({className, fill}) => <Icon className={className} fill={fill || "none"} d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>;
    const X = ({className}) => <Icon className={className} d={<><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></>}/>;
    const MessageSquare = ({className}) => <Icon className={className} d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>;
    const Clock = ({className}) => <Icon className={className} d={<><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></>}/>;
    const BookOpen = ({className}) => <Icon className={className} d={<><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></>}/>;
    const ArrowLeftRight = ({className}) => <Icon className={className} d={<><polyline points="8 3 4 7 8 11"/><polyline points="16 3 20 7 16 11"/><line x1="4" y1="7" x2="20" y2="7"/></>}/>;
    const Bookmark = ({className}) => <Icon className={className} d="M19 21l-7-5-7 5V5a2 2 0 0 1 2-2h10a2 2 0 0 1 2 2z"/>;
    const FastForward = ({className}) => <Icon className={className} d={<><polygon points="13 19 22 12 13 5 13 19" fill="currentColor" stroke="none"/><polygon points="2 19 11 12 2 5 2 19" fill="currentColor" stroke="none"/></>}/>;
    const Rewind = ({className}) => <Icon className={className} d={<><polygon points="11 19 2 12 11 5 11 19" fill="currentColor" stroke="none"/><polygon points="22 19 13 12 22 5 22 19" fill="currentColor" stroke="none"/></>}/>;
    const FileText = ({className}) => <Icon className={className} d={<><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><line x1="10" y1="9" x2="8" y2="9"/></>}/>;
    const Volume2 = ({className}) => <Icon className={className} d={<><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M19.07 4.93a10 10 0 0 1 0 14.14"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/></>}/>;
    const Eye = ({className}) => <Icon className={className} d={<><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></>}/>;
    const ZoomIn = ({className}) => <Icon className={className} d={<><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="11" y1="8" x2="11" y2="14"/><line x1="8" y1="11" x2="14" y2="11"/></>}/>;
    const ZoomOut = ({className}) => <Icon className={className} d={<><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/><line x1="8" y1="11" x2="14" y2="11"/></>}/>;
    const RotateCcw = ({className}) => <Icon className={className} d={<><polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/></>}/>;
    const Maximize2 = ({className}) => <Icon className={className} d={<><polyline points="15 3 21 3 21 9"/><polyline points="9 21 3 21 3 15"/><line x1="21" y1="3" x2="14" y2="10"/><line x1="3" y1="21" x2="10" y2="14"/></>}/>;
    const FileCheck = ({className}) => <Icon className={className} d={<><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><path d="M9 15l2 2 4-4"/></>}/>;
'''

html = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Economics Debate Review — Saint Francis High School</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/react/18.2.0/umd/react.production.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/react-dom/18.2.0/umd/react-dom.production.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/babel-standalone/7.23.9/babel.min.js"></script>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://accounts.google.com/gsi/client" async defer></script>
  <script src="https://apis.google.com/js/api.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>
  <script>pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';</script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,wght@0,700;1,700&family=Barlow:ital,wght@0,400;0,500;0,600;0,700;1,400;1,600&display=swap" rel="stylesheet">
  <script>
    tailwind.config = {
      theme: {
        extend: {
          fontFamily: {
            headline: ['"Source Serif 4"', 'Georgia', 'serif'],
            body: ['Barlow', 'system-ui', 'sans-serif'],
          },
          colors: {
            leather: { DEFAULT: '#48291b', light: '#f5ebe6' },
            cedar: { DEFAULT: '#a16c0d', light: '#faf3e6' },
            sunlight: '#ffc62b',
            fire: '#b66008',
            ash: { 1: '#e3e1de', 2: '#c6c2bd', 3: '#978f85', 4: '#5e5243', 5: '#1f1c1a' },
            dove: '#ffffff',
          }
        }
      }
    }
  </script>
  <style>
    * { scrollbar-width: thin; scrollbar-color: #c6c2bd transparent; }
    *::-webkit-scrollbar { width: 6px; }
    *::-webkit-scrollbar-thumb { background: #c6c2bd; border-radius: 3px; }
    body { margin: 0; font-family: 'Barlow', system-ui, sans-serif; color: #1f1c1a; }
    h1, h2, h3, .sf-headline { font-family: 'Source Serif 4', Georgia, serif; font-weight: 700; }

    /* SFHS Team Color Classes */
    .sf-bg-cedar { background-color: #a16c0d; }
    .sf-bg-cedar-light { background-color: #faf3e6; }
    .sf-text-cedar { color: #a16c0d; }
    .sf-border-cedar { border-color: #c9a34d; }
    .sf-badge-cedar { background-color: #faf3e6; color: #a16c0d; }

    .sf-bg-leather { background-color: #48291b; }
    .sf-bg-leather-light { background-color: #f5ebe6; }
    .sf-text-leather { color: #48291b; }
    .sf-border-leather { border-color: #8b6650; }
    .sf-badge-leather { background-color: #f5ebe6; color: #48291b; }

    /* Active segment tab override */
    .sf-bg-cedar.text-white, .sf-bg-leather.text-white { color: #fff !important; }

    /* Bug Report Widget */
    .bug-fab {
      position: fixed;
      bottom: 24px;
      right: 24px;
      z-index: 9999;
      width: 48px;
      height: 48px;
      border-radius: 50%;
      background: #48291b;
      color: white;
      border: none;
      cursor: pointer;
      box-shadow: 0 4px 12px rgba(0,0,0,0.3);
      display: flex;
      align-items: center;
      justify-content: center;
      transition: transform 0.2s, background 0.2s;
    }
    .bug-fab:hover { transform: scale(1.1); background: #5a3525; }
    .bug-report-panel {
      position: fixed;
      bottom: 84px;
      right: 24px;
      z-index: 9998;
      width: 360px;
      background: white;
      border-radius: 12px;
      box-shadow: 0 8px 32px rgba(0,0,0,0.2);
      border: 1px solid #e3e1de;
      overflow: hidden;
    }
  </style>
</head>
<body>
  <div id="root"></div>
  <script type="text/babel">
    const { useState, useEffect, useRef, useCallback, useMemo } = React;
''' + icons + '\n' + jsx_code + '''

    const root = ReactDOM.createRoot(document.getElementById('root'));
    root.render(React.createElement(App));
  </script>
</body>
</html>'''

with open('/sessions/sleepy-confident-bell/mnt/Downloads/index.html', 'w') as f:
    f.write(html)

print(f"Written index.html: {len(html)} chars, {html.count(chr(10))} lines")
