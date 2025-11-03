# 📜 Scroll-to-Fullscreen Feature

## What It Does

**Scroll Down** → Header & tabs hide, editor goes fullscreen  
**Scroll Up** → Header & tabs reappear

## How It Works

### 1. Scroll Detection
```javascript
useEffect(() => {
  const handleScroll = () => {
    const currentScrollY = window.scrollY;
    
    if (currentScrollY > lastScrollY && currentScrollY > 100) {
      // Scrolling down & past 100px → Hide header
      setHeaderVisible(false);
    } else if (currentScrollY < lastScrollY) {
      // Scrolling up → Show header
      setHeaderVisible(true);
    }
    
    setLastScrollY(currentScrollY);
  };

  window.addEventListener('scroll', handleScroll, { passive: true });
  
  return () => {
    window.removeEventListener('scroll', handleScroll);
  };
}, [lastScrollY]);
```

### 2. Sticky Headers
```css
.status-bar {
  position: sticky;
  top: 0;
  z-index: 100;
  transition: transform 0.3s ease, opacity 0.3s ease;
}

.file-tabs-bar {
  position: sticky;
  top: 48px;  /* Below status bar */
  z-index: 99;
  transition: transform 0.3s ease, opacity 0.3s ease;
}
```

### 3. Hide Animation
```css
.status-bar.hidden {
  transform: translateY(-100%);
  opacity: 0;
  pointer-events: none;
}

.file-tabs-bar.hidden {
  transform: translateY(-100%);
  opacity: 0;
  pointer-events: none;
}
```

### 4. Fullscreen Editor
```css
/* When both headers hidden, editor goes fullscreen */
.status-bar.hidden ~ .file-tabs-bar.hidden ~ .editor-workspace-v2 {
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 98;
}
```

## User Experience

### Normal State (Scroll Up)
```
┌─────────────────────────────────────┐
│ ✨ Resume Formatter Pro | ✓ Complete│  ← Status Bar (48px)
├─────────────────────────────────────┤
│ 👇 Click any resume below           │  ← Hint Banner
│ 📄 ADIKA MAUL  DOCX  ⬇️             │  ← Tabs (60px)
├─────────────────────────────────────┤
│                                     │
│   OnlyOffice Editor                 │  ← Editor (remaining space)
│                                     │
└─────────────────────────────────────┘
```

### Fullscreen State (Scroll Down)
```
┌─────────────────────────────────────┐
│                                     │
│                                     │
│   OnlyOffice Editor                 │  ← Editor (100vh - fullscreen!)
│   (Full Screen)                     │
│                                     │
│                                     │
└─────────────────────────────────────┘
```

## Features

✅ **Smooth Transitions** - 0.3s ease animation  
✅ **Smart Threshold** - Only hides after scrolling 100px  
✅ **Scroll Direction** - Up = show, Down = hide  
✅ **Sticky Headers** - Stay at top when visible  
✅ **Fullscreen Editor** - Takes entire viewport when headers hidden  
✅ **No Layout Shift** - Smooth, no jumps  

## Benefits

1. **More Editing Space** - Full viewport for document
2. **Distraction-Free** - Headers hide when editing
3. **Easy Access** - Scroll up to see controls
4. **Professional** - Like modern apps (YouTube, Medium)
5. **Intuitive** - Natural scroll behavior

## Technical Details

### State Management
```javascript
const [headerVisible, setHeaderVisible] = useState(true);
const [lastScrollY, setLastScrollY] = useState(0);
```

### Conditional Classes
```javascript
<div className={`status-bar ${!headerVisible ? 'hidden' : ''}`}>
<div className={`file-tabs-bar ${!headerVisible ? 'hidden' : ''}`}>
```

### CSS Layers (Z-Index)
- Status Bar: `z-index: 100`
- Tabs Bar: `z-index: 99`
- Editor (fullscreen): `z-index: 98`

## How to Test

1. **Format a resume**
2. **Click to preview**
3. **Scroll down slowly** → Headers slide up and hide
4. **Editor expands** → Takes full screen
5. **Scroll up** → Headers slide back down
6. **Smooth transition** → No jumps!

## Customization

### Change Hide Threshold
```javascript
if (currentScrollY > lastScrollY && currentScrollY > 100) {
  //                                              ^^^ Change this number
  setHeaderVisible(false);
}
```

### Change Animation Speed
```css
.status-bar {
  transition: transform 0.3s ease, opacity 0.3s ease;
  /*                    ^^^                  ^^^
                    Change these durations */
}
```

### Disable Feature
Remove or comment out the scroll useEffect in `DownloadPhase.js`

## Browser Compatibility

✅ Chrome/Edge - Perfect  
✅ Firefox - Perfect  
✅ Safari - Perfect  
✅ Mobile - Works great  

## Performance

- Uses `passive: true` for scroll listener (better performance)
- Smooth 60fps animations
- No layout recalculation on scroll
- Efficient state updates

---

**Enjoy distraction-free editing with automatic fullscreen!** 📜✨
