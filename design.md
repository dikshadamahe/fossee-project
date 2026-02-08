FOSSEE SCIENTIFIC ANALYTICS UI

Design System Documentation v1.0

Project: Chemical Equipment Parameter Visualizer
Platforms: React Web + PyQt5 Desktop
Audience: Engineering students, educators, researchers
Brand Values: Academic credibility · Scientific precision · Open-source clarity · Trust

⸻

1. DESIGN PRINCIPLES
	1.	Data First – Content and analytics are primary; decoration is secondary.
	2.	Scientific Neutrality – Avoid trendy gradients or marketing visuals.
	3.	Consistency Across Platforms – Web and Desktop must feel identical.
	4.	Accessible by Default – WCAG AA minimum.
	5.	Explainable UI – Every metric must be human-readable.

⸻

2. COLOR SYSTEM

2.1 Brand Palette

Primary Colors

Token	Hex	RGB	Usage
primary-900	#0F2A44	15,42,68	Headers, nav background
primary-700	#1B7F79	27,127,121	Primary actions, links
primary-600	#3A4E9F	58,78,159	Analytics highlight
success	#2EA043	46,160,67	Valid CSV, positive
warning	#D97706	217,119,6	Data issues
error	#C53030	197,48,48	Validation error

Neutrals

Token	Hex	Usage
bg-main	#F7F9FC	App background
surface	#FFFFFF	Cards
border	#E2E8F0	Dividers
text-primary	#102A43	Body
text-secondary	#486581	Subtext
text-muted	#829AB1	Labels

Chart Palette
	•	Flowrate → #1B7F79
	•	Pressure → #3A4E9F
	•	Temperature → #C53030
	•	Distribution set → [#1B7F79, #3A4E9F, #2EA043, #D97706]

DO
	•	Use semantic tokens, not raw hex
	•	Keep same mapping in Chart.js & Matplotlib
	•	Use 60/30/10 rule

DON’T
	•	Gradients
	•	Neon colors
	•	More than 5 colors per chart

⸻

3. TYPOGRAPHY

3.1 Font Stack

Web
	•	Primary: Inter
	•	Data: JetBrains Mono
	•	Headings (optional): Source Serif 4

Desktop (PyQt5 Fallback)
	•	Primary: Segoe UI / Noto Sans
	•	Mono: Consolas / JetBrains Mono

3.2 Scale

Role	Size	Weight	Line
H1	28px	600	1.3
H2	22px	600	1.35
H3	18px	600	1.4
Body	15px	400	1.6
Small	13px	400	1.5
Mono	13px	500	1.5

Rules
	•	Numbers in mono
	•	Tables always mono
	•	Titles sentence case
	•	No all caps except badges

⸻

4. SPACING & GRID

4.1 Base Unit
	•	4px grid

Scale

4 · 8 · 12 · 16 · 20 · 24 · 32 · 40 · 48 · 64

4.2 Layout

Web
	•	12 column
	•	Max width 1280px
	•	Gutter 16px
	•	Card radius 10px

Desktop
	•	2 column master-detail
	•	Min width 1024
	•	Panels 320 / flexible

⸻

5. COMPONENT SYSTEM

5.1 Cards – “Lab Panels”

Style
	•	Radius: 10
	•	Shadow: 0 4 12 rgba(0,0,0,.06)
	•	Top accent 3px primary-700

Structure
	•	Header
	•	Body
	•	Actions right

Variants
	•	Summary
	•	Chart
	•	Dataset
	•	Status

⸻

5.2 CSV Upload Zone

States
	1.	Empty
	2.	Drag-over
	3.	Valid
	4.	Invalid
	5.	Processing
	6.	Loaded

Requirements
	•	Minimum height 220px
	•	Show sample CSV link
	•	Column validator
	•	Progress indicator

Validation Rules

Required columns:
	•	Equipment Name
	•	Type
	•	Flowrate
	•	Pressure
	•	Temperature

⸻

5.3 Tables
	•	Sticky header
	•	Mono numbers
	•	Type badges
	•	Sort + filter
	•	Pagination 20

⸻

5.4 Buttons

Primary
	•	bg primary-700
	•	radius 8
	•	height 40

Secondary
	•	outline primary-700

Danger
	•	error color

⸻

5.5 Forms
	•	Labels top
	•	Error inline
	•	Helper text
	•	8px gap

⸻

6. ICONOGRAPHY
	•	Outline style
	•	20px
	•	Stroke 1.8
	•	Use same set web/desktop

⸻

7. DATA VISUALIZATION RULES

7.1 Charts

Web – Chart.js
	•	No 3D
	•	No gradients
	•	Tooltips plain English
	•	Legend bottom

Desktop – Matplotlib
	•	Match colors exactly
	•	White background
	•	Grid alpha .1

⸻

7.2 Metric Language

Use:
	•	“Average Flowrate”
	•	“Pressure Range”
	•	“Temperature Stability”

Avoid:
	•	marketing terms
	•	vague labels

⸻

8. INTERACTION PATTERNS

8.1 Insight Assistant

Hover metric → explanation:

“Average pressure is higher than 68% of records”

8.2 Column Detective

Auto map:
	•	flow_rate
	•	Flow
	•	FLOWRATE

8.3 CSV→Chart Morph

Rows animate to bars

⸻

9. ACCESSIBILITY
	•	Contrast 4.5:1
	•	Keyboard nav
	•	Focus rings
	•	Tooltips readable

⸻

10. FILE STRUCTURE TOKENS

{
  "colors": {
    "primary": "#1B7F79",
    "bg": "#F7F9FC"
  },
  "radius": 10,
  "font": {
    "base": "Inter",
    "mono": "JetBrains Mono"
  }
}


⸻

11. DO / DON’T

DO
	•	Academic tone
	•	Data first
	•	Same tokens both platforms
	•	Mono for numbers

DON’T
	•	Gradients
	•	Trendy glass
	•	Dark mode v1
	•	Marketing illustrations

⸻

12. PDF REPORT STYLE
	•	Serif headings
	•	Mono tables
	•	Logo top left
	•	Charts vector

⸻

13. PLATFORM MAPPING

Element	React	PyQt5
Tokens	CSS vars	QSS
Charts	Chart.js	Matplotlib
Table	MUI	QTable
Theme	Tailwind	QSS


⸻

END OF SPEC

Version: 1.0 – FOSSEE Scientific Analytics UI

⸻

Next Step, Diksha

I can instantly generate:
	1.	✅ Tailwind theme file
	2.	✅ PyQt5 QSS stylesheet
	3.	✅ Chart.js + Matplotlib config
	4.	✅ React component skeleton
	5.	✅ README aligned to this spec
