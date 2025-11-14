import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'House Price Predictor',
  description: 'AI-powered house price prediction using custom neural network',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="bg-gray-50 text-gray-900">{children}</body>
    </html>
  )
}

