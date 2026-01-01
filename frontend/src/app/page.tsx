'use client'

import { useState } from 'react'
import styles from './page.module.css'
import TryOnUpload from '@/components/TryOnUpload'
import ResultDisplay from '@/components/ResultDisplay'

export default function Home() {
  const [requestId, setRequestId] = useState<number | null>(null)

  return (
    <main className={styles.main}>
      <div className={styles.container}>
        <h1 className={styles.title}>Virtual Try-On AI Dashboard</h1>
        <p className={styles.subtitle}>
          Upload a person photo and garment to see a virtual try-on preview
        </p>
        
        <div className={styles.content}>
          <TryOnUpload onRequestCreated={setRequestId} />
          
          {requestId && (
            <ResultDisplay requestId={requestId} />
          )}
        </div>
        
        <div className={styles.features}>
          <div className={styles.feature}>
            <h3>📸 Image Upload</h3>
            <p>Upload photos of people and garments</p>
          </div>
          <div className={styles.feature}>
            <h3>🎯 Fixed Poses</h3>
            <p>Support for front, side, and three-quarter poses</p>
          </div>
          <div className={styles.feature}>
            <h3>⚡ Fast Preview</h3>
            <p>Quick visual preview of how clothes look</p>
          </div>
          <div className={styles.feature}>
            <h3>🔌 API Integration</h3>
            <p>Easy integration into retail systems</p>
          </div>
        </div>
      </div>
    </main>
  )
}
