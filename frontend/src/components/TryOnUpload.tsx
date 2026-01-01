'use client'

import { useState } from 'react'
import styles from './TryOnUpload.module.css'
import { createTryOnRequest } from '@/services/api'

interface TryOnUploadProps {
  onRequestCreated: (requestId: number) => void
}

export default function TryOnUpload({ onRequestCreated }: TryOnUploadProps) {
  const [personImage, setPersonImage] = useState<File | null>(null)
  const [garmentImage, setGarmentImage] = useState<File | null>(null)
  const [pose, setPose] = useState<'front' | 'side' | 'three-quarter'>('front')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!personImage || !garmentImage) {
      setError('Please upload both person and garment images')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const response = await createTryOnRequest(personImage, garmentImage, pose)
      onRequestCreated(response.request_id)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create try-on request')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className={styles.container}>
      <h2 className={styles.heading}>Upload Images</h2>
      
      <form onSubmit={handleSubmit} className={styles.form}>
        <div className={styles.uploadGroup}>
          <div className={styles.uploadBox}>
            <label htmlFor="person-image" className={styles.label}>
              Person Image
            </label>
            <input
              id="person-image"
              type="file"
              accept="image/*"
              onChange={(e) => setPersonImage(e.target.files?.[0] || null)}
              className={styles.fileInput}
            />
            {personImage && (
              <p className={styles.fileName}>{personImage.name}</p>
            )}
          </div>

          <div className={styles.uploadBox}>
            <label htmlFor="garment-image" className={styles.label}>
              Garment Image
            </label>
            <input
              id="garment-image"
              type="file"
              accept="image/*"
              onChange={(e) => setGarmentImage(e.target.files?.[0] || null)}
              className={styles.fileInput}
            />
            {garmentImage && (
              <p className={styles.fileName}>{garmentImage.name}</p>
            )}
          </div>
        </div>

        <div className={styles.poseSelector}>
          <label className={styles.label}>Select Pose</label>
          <div className={styles.poseOptions}>
            <label className={styles.poseOption}>
              <input
                type="radio"
                value="front"
                checked={pose === 'front'}
                onChange={(e) => setPose(e.target.value as 'front')}
              />
              Front
            </label>
            <label className={styles.poseOption}>
              <input
                type="radio"
                value="side"
                checked={pose === 'side'}
                onChange={(e) => setPose(e.target.value as 'side')}
              />
              Side
            </label>
            <label className={styles.poseOption}>
              <input
                type="radio"
                value="three-quarter"
                checked={pose === 'three-quarter'}
                onChange={(e) => setPose(e.target.value as 'three-quarter')}
              />
              Three-Quarter
            </label>
          </div>
        </div>

        {error && <div className={styles.error}>{error}</div>}

        <button
          type="submit"
          disabled={loading || !personImage || !garmentImage}
          className={styles.submitButton}
        >
          {loading ? 'Processing...' : 'Generate Try-On'}
        </button>
      </form>
    </div>
  )
}
