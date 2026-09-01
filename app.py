# 🎨 PhotoTag Pro - Style Guide & Design Tokens

## Color System

### Primary Brand Colors
```
Primary Blue:       #2563eb  RGB(37, 99, 235)   - Main CTA, Interactive elements
Primary Dark:       #1e40af  RGB(30, 64, 175)   - Hover states, Depth
Accent Indigo:      #6366f1  RGB(99, 102, 241) - Secondary elements
Success Green:      #10b981  RGB(16, 185, 129) - Success states, Validation
Alert Orange:       #f59e0b  RGB(245, 158, 11) - Warnings
```

### Neutral Palette
```
Text Dark:          #0f172a  RGB(15, 23, 42)   - Headlines, Primary text
Text Gray:          #64748b  RGB(100, 116, 139) - Secondary text, Labels
Border Light:       #e2e8f0  RGB(226, 232, 240) - Subtle dividers
Background Soft:    #f8fafc  RGB(248, 250, 252) - Main background
Background Lighter: #f1f5f9  RGB(241, 245, 249) - Secondary background (gradient)
White:              #ffffff  RGB(255, 255, 255) - Card backgrounds
```

### Semantic Color Mapping
| Color | Usage | Hex | RGB |
|-------|-------|-----|-----|
| Primary | Buttons, Links, Focus states | #2563eb | 37, 99, 235 |
| Success | Validation, Check marks, Confirmations | #10b981 | 16, 185, 129 |
| Warning | Alerts, Cautions | #f59e0b | 245, 158, 11 |
| Error | Errors (if needed) | #ef4444 | 239, 68, 68 |
| Info | Informational messages | #2563eb | 37, 99, 235 |

---

## Typography System

### Font Family
```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 
             Roboto, 'Helvetica Neue', sans-serif;
```
**Rationale:** System font stack loads instantly, optimized rendering per OS

### Type Scale
```
Headline 1 (H1):     2.5rem / 40px  - Weight 800 - Letter-spacing -0.5px
Headline 2 (H2):     1.3rem / 21px  - Weight 700 - Line-height 1.2
Subheading (H3):     1.1rem / 18px  - Weight 600 - Line-height 1.3
Body Large:          1rem / 16px    - Weight 400 - Line-height 1.6
Body Regular:        0.95rem / 15px - Weight 400 - Line-height 1.5
Body Small:          0.9rem / 14px  - Weight 400 - Line-height 1.4
Label:               0.85rem / 13px - Weight 600 - Line-height 1.2
Caption:             0.75rem / 12px - Weight 500 - Line-height 1.2
```

### Font Weight Scale
```
Light:       300  (Not typically used)
Regular:     400  (Body text, general content)
Medium:      500  (Captions, subtle emphasis)
SemiBold:    600  (Labels, button text, small headings)
Bold:        700  (Card titles, stronger emphasis)
ExtraBold:   800  (Page title, major headings)
```

### Line Height Scale
```
Tight:       1.2  (Headlines, compact text)
Normal:      1.5  (Body text)
Relaxed:     1.6  (Large body, improved readability)
```

---

## Spacing System (8px Base Unit)

```
0     = 0px
1     = 8px   (tight spacing between elements)
2     = 16px  (standard padding inside components)
3     = 24px  (spacing between card content)
4     = 32px  (card padding, section spacing)
5     = 40px  (large section spacing)
6     = 48px  (header spacing)
```

### Applied Spacing
```
Card padding:          4 (32px) on all sides
Input padding:         12px horizontal, 12px vertical (1.5x = 12px)
Button padding:        1.5 vertical (12px), 3 horizontal (24px)
Section gap:           32px (4 units)
Small element gap:     16px (2 units)
Header margin-bottom:  50px (6.25 units)
```

---

## Component Specifications

### Cards
```css
Background:      #ffffff
Padding:         32px
Border:          1px solid #e2e8f0
Border-radius:   12px
Box-shadow:      0 1px 3px rgba(0, 0, 0, 0.08)
Box-shadow hover:0 4px 12px rgba(0, 0, 0, 0.1)
Transition:      0.3s cubic-bezier(0.4, 0, 0.2, 1)
```

### Buttons (Primary CTA)
```css
Background:      Linear gradient (from #2563eb to #1e40af)
Color:           #ffffff
Padding:         12px 24px
Border:          none
Border-radius:   8px
Font:            600 weight, 1rem size
Box-shadow:      0 2px 8px rgba(37, 99, 235, 0.3)
Box-shadow hover:0 4px 16px rgba(37, 99, 235, 0.4)
Transform hover: translateY(-1px)
Transition:      0.2s all
Cursor:          pointer
```

### Input Fields (Text & Textarea)
```css
Background:      #ffffff
Border:          1.5px solid #e2e8f0
Border-radius:   8px
Padding:         12px 14px
Font-size:       0.95rem
Color:           #0f172a
Border focus:    #2563eb
Shadow focus:    0 0 0 3px rgba(37, 99, 235, 0.1)
Transition:      0.2s all
```

### Info Box / Alert Container
```css
Background:      Linear gradient (from rgba(37,99,235,0.05) to rgba(99,102,241,0.05))
Border-left:     3px solid #2563eb
Padding:         16px
Border-radius:   8px
Font-size:       0.95rem
Line-height:     1.5
Color:           #0f172a
```

### Step Indicator Badge
```css
Width:           32px
Height:          32px
Border-radius:   50% (circle)
Background:      #2563eb
Color:           #ffffff
Font-size:       0.9rem
Font-weight:     700
Display:         flex (center align)
```

---

## Shadow Elevation Scale

Used to create depth and hierarchy:

```
Elevation 1: 0 1px 3px rgba(0, 0, 0, 0.08)
             (Card default, subtle depth)

Elevation 2: 0 4px 12px rgba(0, 0, 0, 0.1)
             (Card hover, increased depth)

Elevation 3: 0 8px 24px rgba(0, 0, 0, 0.12)
             (Not currently used, available for future)

Elevation 4: 0 12px 32px rgba(0, 0, 0, 0.15)
             (Not currently used, for modal dialogs if added)
```

---

## Animation & Transition Guidelines

### Duration
```
Quick:         0.15s (micro-interactions)
Standard:      0.2s  (hover states, quick transitions)
Smooth:        0.3s  (page enter, card animations)
Slow:          0.5s  (important state changes)
```

### Easing Functions
```
ease-out:           Cubic-bezier(0.4, 0, 0.2, 1)  - User initiated animations
ease-in-out:        Cubic-bezier(0.4, 0, 0.2, 1)  - Page transitions
ease-linear:        Cubic-bezier(0, 0, 1, 1)      - Loading indicators
```

### Animations Defined
```
fadeInDown:  opacity & translateY(-20px) → 0%, 0px  (0.6s ease-out)
slideUp:     opacity & translateY(20px) → 0%, 0px   (0.5s ease-out)
```

---

## Border Radius Scale

```
Sharp:       0px    (Not used in modern design)
Tiny:        4px    (Not used in this design)
Small:       8px    (Buttons, input fields)
Medium:      12px   (Cards, larger containers)
Round:       50%    (Circles - badges, avatars)
```

---

## Layout Grid

### Main Container
```
Max-width:        No max constraint (full width responsive)
Padding:          40px horizontal on large screens
Padding mobile:   20px horizontal
Margin:           0 (edge to edge)
```

### Two-Column Layout
```
Grid:             1fr 1fr (equal columns)
Gap:              32px (4 spacing units)
Min-width col:    Responsive, no minimum per column
Responsive break: 1200px breakpoint → stacks to 1fr
```

### Metrics Row
```
Grid:             2 equal columns
Gap:              16px
Responsive:       Stays 2 columns on mobile (tight but functional)
```

---

## Icon/Emoji Usage

### Semantic Icons
```
📸    Photo/Camera        - Visual identifier for photo app
🚀    Launch/Rocket       - Action CTA "Process"
✅    Check mark          - Success confirmation
⚠️    Warning triangle    - Alert/warning messages
💡    Bulb               - Tips/helpful information
📤    Upload arrow        - File upload action
📥    Download arrow      - File download action
🔄    Reset/Refresh       - Retry/redo action
⏳    Hourglass          - Loading/processing state
📐    Ruler              - Design/technical indicator
🎨    Palette            - Design/style related
```

**Usage Rule:** Use sparingly, only where they add meaning. Don't decorate unnecessarily.

---

## Accessibility Standards

### Color Contrast
- All text: Minimum 4.5:1 (WCAG AA)
- Large text: Minimum 3:1 (WCAG AA)

Example passes:
- Dark text (#0f172a) on white (#ffffff): 15.31:1 ✅
- Primary blue (#2563eb) text on white: 5.2:1 ✅
- Secondary gray (#64748b) on white: 5.1:1 ✅

### Touch Targets
- Minimum size: 44px × 44px (iOS) / 48dp (Android)
- Button area: Padding ensures adequate touch zone
- Spacing: Minimum 8px between interactive elements

### Keyboard Navigation
- Focus states clearly visible
- Focus outline: 3px rgba(37, 99, 235, 0.1) shadow
- Tab order logical

---

## Responsive Breakpoints

```
Mobile:           < 640px    (Phone vertical)
Tablet:           640-1024px (Phone horizontal, tablet)
Desktop:          > 1024px   (Standard desktop)
Layout shift:     1200px     (Two-column to one-column)
```

### Key Breakpoints in Design
```css
@media (max-width: 1200px) {
    .two-column { grid-template-columns: 1fr; }
}
```

---

## Color Palette (Quick Reference)

### Primary Action
```
Default:  #2563eb (RGB 37, 99, 235)
Hover:    #1e40af (RGB 30, 64, 175)
Active:   #1e40af (same as hover)
Focus:    @shadow 0 0 0 3px rgba(37, 99, 235, 0.1)
Disabled: rgba(37, 99, 235, 0.5)
```

### Semantic
```
Success:  #10b981 (RGB 16, 185, 129)
Warning:  #f59e0b (RGB 245, 158, 11)
Error:    #ef4444 (RGB 239, 68, 68)
Info:     #2563eb (same primary blue)
```

### Text
```
Headings:  #0f172a (RGB 15, 23, 42) - High contrast
Body:      #0f172a (RGB 15, 23, 42) - High contrast
Secondary: #64748b (RGB 100, 116, 139) - Medium contrast
Disabled:  rgba(100, 116, 139, 0.5) - Low contrast
```

---

## State Specifications

### Button States
```
Normal:    Base gradient, normal shadow
Hover:     Enhanced shadow, translateY(-1px)
Active:    No transform, visual depression
Focus:     Box shadow outline (focus-visible)
Disabled:  Reduced opacity, not interactive
Loading:   Spinner, text may change
```

### Input States
```
Idle:      Border #e2e8f0, no shadow
Focus:     Border #2563eb, shadow 0 0 0 3px rgba(37, 99, 235, 0.1)
Valid:     Border #10b981 (optional visual validation)
Invalid:   Border #ef4444 (error state)
Disabled:  Background #f8fafc, border opacity 0.5
```

### Card States
```
Default:   Shadow elevation 1
Hover:     Shadow elevation 2, subtle scale
Active:    No visual change (unless linked)
Disabled:  Opacity 0.5
```

---

## Code Implementation Standards

### CSS Custom Properties Template
```css
:root {
    --primary: #2563eb;
    --primary-dark: #1e40af;
    --text-primary: #0f172a;
    --text-secondary: #64748b;
    --bg-light: #f8fafc;
    --bg-card: #ffffff;
    --border: #e2e8f0;
}
```

### Selector Naming Convention
```
.card              - Card container
.card-title        - Title within card
.card:hover        - Hover state
.step-indicator    - Step badge
.info-box          - Information container
.preview-label     - Preview section label
.preview-container - Preview image container
.animate-in        - Animation class
```

---

## Maintenance Checklist

- ✅ All colors defined in :root
- ✅ All animations in @keyframes
- ✅ All breakpoints clearly marked
- ✅ No hardcoded colors in components
- ✅ Consistent naming conventions
- ✅ Documented easing functions
- ✅ Shadow elevation scale defined
- ✅ Spacing system documented
- ✅ Typography scale locked

---

**Version:** 1.0
**Last Updated:** September 2026
**Maintained by:** Design System Team
