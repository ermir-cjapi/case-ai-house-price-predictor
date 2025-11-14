import { NextRequest, NextResponse } from 'next/server'

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:5000'

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    const { model_type = 'tensorflow', async = true, ...trainParams } = body

    // Determine endpoint based on async flag
    const endpoint = async 
      ? `${BACKEND_URL}/train/${model_type}/async`
      : `${BACKEND_URL}/train/${model_type}`

    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(trainParams),
    })

    const data = await response.json()

    return NextResponse.json(data, { status: response.status })
  } catch (error) {
    console.error('Training API error:', error)
    return NextResponse.json(
      {
        success: false,
        message: 'Failed to connect to backend service',
      },
      { status: 500 }
    )
  }
}

