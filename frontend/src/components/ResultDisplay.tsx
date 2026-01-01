'use client'

import { useEffect, useState } from 'react'
import styles from './ResultDisplay.module.css'
import { getTryOnRequest } from '@/services/api'

interface ResultDisplayProps {
  requestId: number
}

interface TryOnResult {
  id: number
  status: string
  result_image_path: string | null
  error_message: string | null
  processing_time: number | null
}

export default function ResultDisplay({ requestId }: ResultDisplayProps) {
  const [result, setResult] = useState<TryOnResult | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let interval: NodeJS.Timeout

    const fetchResult = async () => {
      try {
        const data = await getTryOnRequest(requestId)
        setResult(data)
        
        // If completed or failed, stop polling
        if (data.status === 'completed' || data.status === 'failed') {
          setLoading(false)
          if (interval) clearInterval(interval)
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch result')
        setLoading(false)
        if (interval) clearInterval(interval)
      }
    }

    // Initial fetch
    fetchResult()

    // Poll every 2 seconds while processing
    interval = setInterval(fetchResult, 2000)

    return () => {
      if (interval) clearInterval(interval)
    }
  }, [requestId])

  if (error) {
    return (
      <div className={styles.container}>
        <div className={styles.error}>{error}</div>
      </div>
    )
  }

  if (!result) {
    return (
      <div className={styles.container}>
        <div className={styles.loading}>Loading...</div>
      </div>
    )
  }

  return (
    <div className={styles.container}>
      <h2 className={styles.heading}>Try-On Result</h2>
      
      <div className={styles.statusBadge} data-status={result.status}>
        Status: {result.status.toUpperCase()}
      </div>

      {result.status === 'processing' && (
        <div className={styles.processing}>
          <div className={styles.spinner}></div>
          <p>Processing your try-on request...</p>
        </div>
      )}

      {result.status === 'completed' && result.result_image_path && (
        <div className={styles.resultImage}>
          <img
            src={`http://localhost:8000/${result.result_image_path}`}
            alt="Try-on result"
          />
          {result.processing_time && (
            <p className={styles.processingTime}>
              Processing time: {result.processing_time.toFixed(2)}s
            </p>
          )}
        </div>
      )}

      {result.status === 'failed' && (
        <div className={styles.errorMessage}>
          <p>❌ Try-on failed</p>
          {result.error_message && (
            <p className={styles.errorDetail}>{result.error_message}</p>
          )}
        </div>
      )}
    </div>
  )
}
