import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

export interface TryOnResponse {
  request_id: number
  status: string
  result_image_url: string | null
  message: string
  created_at: string
}

export interface TryOnRequestDetail {
  id: number
  user_image_path: string
  garment_image_path: string
  result_image_path: string | null
  pose: string
  status: string
  created_at: string
  updated_at: string
  error_message: string | null
  processing_time: number | null
}

export async function createTryOnRequest(
  personImage: File,
  garmentImage: File,
  pose: string
): Promise<TryOnResponse> {
  const formData = new FormData()
  formData.append('person_image', personImage)
  formData.append('garment_image', garmentImage)
  formData.append('pose', pose)

  const response = await axios.post<TryOnResponse>(
    `${API_BASE_URL}/tryon/`,
    formData,
    {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    }
  )

  return response.data
}

export async function getTryOnRequest(requestId: number): Promise<TryOnRequestDetail> {
  const response = await axios.get<TryOnRequestDetail>(
    `${API_BASE_URL}/tryon/${requestId}`
  )
  return response.data
}

export async function listTryOnRequests(
  skip: number = 0,
  limit: number = 10
): Promise<TryOnRequestDetail[]> {
  const response = await axios.get<TryOnRequestDetail[]>(
    `${API_BASE_URL}/tryon/`,
    {
      params: { skip, limit },
    }
  )
  return response.data
}
