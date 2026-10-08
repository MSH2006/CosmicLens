export default function HomePage() {
  return (
    <main style={{ padding: '2rem', fontFamily: 'sans-serif', background: '#020b12', color: '#eaf6ff', minHeight: '100vh' }}>
      <div style={{ maxWidth: 980, margin: '0 auto' }}>
        <p style={{ letterSpacing: '0.2em', textTransform: 'uppercase', color: '#8abfed', marginBottom: '1rem' }}>
          NASA SPHEREx Discovery Prototype
        </p>
        <h1 style={{ fontSize: '3rem', marginBottom: '1rem' }}>CosmicLens</h1>
        <p style={{ fontSize: '1.1rem', lineHeight: 1.7, maxWidth: 760, color: '#d9ebff' }}>
          Explainable AI for Discovering and Understanding Change in the Infrared Sky.
        </p>
        <div style={{ marginTop: '2rem', display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
          <div style={{ background: '#0d1a24', border: '1px solid #1a2f3f', borderRadius: 12, padding: '1rem 1.2rem', minWidth: 220 }}>
            <strong>Phase 0</strong>
            <div style={{ color: '#9ecaf1', marginTop: 8 }}>Project foundation is live.</div>
          </div>
          <div style={{ background: '#0d1a24', border: '1px solid #1a2f3f', borderRadius: 12, padding: '1rem 1.2rem', minWidth: 220 }}>
            <strong>Next step</strong>
            <div style={{ color: '#9ecaf1', marginTop: 8 }}>Sky explorer + time machine</div>
          </div>
        </div>
      </div>
    </main>
  );
}
