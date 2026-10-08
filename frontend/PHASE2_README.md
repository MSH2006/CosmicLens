# CosmicLens Frontend — Phase 2

The frontend now includes:
- Interactive sky explorer with moving objects
- Timeline with epoch playback (Sky Time Machine)
- Real-time data fetching from backend API
- Anomaly analysis display
- Scientific discovery passport summary
- NASA-inspired dark UI design
- Responsive design for desktop/tablet/mobile

## Local Setup

### Prerequisites
- Node.js 18+ installed
- Backend API running on `http://localhost:8000`

### Installation & Running

```bash
cd frontend
npm install
npm run dev
```

Then open:
```
http://localhost:3000
```

### Expected behavior

1. Page loads with "CosmicLens" heading
2. Sky explorer shows a single yellow object (RW-001)
3. Timeline shows 4 epochs (T1, T2, T3, T4)
4. Right panel shows:
   - Anomaly score (should be ~79-90/100)
   - Confidence (should be ~100%)
   - Why interesting (reasons from AI)
   - Artifact risk (LOW)
   - Scientific passport ID
5. Click "Play Sky Time Machine" to animate the object moving across epochs
6. Click individual timeline items to jump to that epoch

### Troubleshooting

**"Connection Error" message:**
- Make sure backend is running on `http://localhost:8000`
- Verify backend health: `curl http://localhost:8000/api/health`

**Object doesn't move:**
- Check browser console for errors (F12 → Console tab)
- Verify backend returns motion data

**Blank page or styling issues:**
- Clear browser cache (Ctrl+Shift+Delete)
- Restart dev server: `npm run dev`

## File Structure

```
frontend/
├── app/
│   ├── page.tsx           Main interactive component
│   ├── globals.css        Complete styling
│   ├── layout.tsx         Root layout
│   └── ...
├── package.json
├── tsconfig.json
└── ...
```

## Next Steps

Once Phase 2 is verified locally:
- [ ] Backend API running on port 8000
- [ ] Frontend running on port 3000
- [ ] Sky explorer loads with data
- [ ] Timeline animation works
- [ ] Anomaly scores display correctly

Then proceed to Phase 3 (Polish & Report Generation)
