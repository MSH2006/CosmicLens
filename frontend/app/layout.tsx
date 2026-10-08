import './globals.css';

export const metadata = {
  title: 'CosmicLens',
  description: 'Explainable AI for Discovering and Understanding Change in the Infrared Sky.',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
