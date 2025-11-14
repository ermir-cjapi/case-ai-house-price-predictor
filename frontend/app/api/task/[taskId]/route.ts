import { NextRequest, NextResponse } from 'next/server'

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:5000'

export async function GET(
  request: NextRequest,
  { params }: { params: { taskId: string } }
) {
  try {
    const taskId = params.taskId

    const response = await fetch(`${BACKEND_URL}/task/${taskId}/status`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })

    const data = await response.json()

    return NextResponse.json(data, { status: response.status })
  } catch (error) {
    console.error('Task status API error:', error)
    return NextResponse.json(
      {
        success: false,
        message: 'Failed to connect to backend service',
      },
      { status: 500 }
    )
  }
}

