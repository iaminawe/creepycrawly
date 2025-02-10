import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { CrawlConfigForm } from "@/components/CrawlConfigForm"
import { CrawlStatus } from "@/components/CrawlStatus"
import { RecentContent } from "@/components/RecentContent"

interface FormValues {
  url: string
  s3Bucket: string
  skipDocs: boolean
}

export default function App() {
  const [isRunning, setIsRunning] = useState(false)
  const [currentUrl, setCurrentUrl] = useState<string>("")

  const handleStartCrawl = async (values: FormValues) => {
    setIsRunning(true)
    setCurrentUrl(values.url)
    
    try {
      // The actual API call is handled in the CrawlConfigForm component
      // This function just updates the UI state
    } catch (error) {
      console.error('Error during crawl:', error)
    } finally {
      setIsRunning(false)
    }
  }

  return (
    <div className="min-h-screen bg-background p-8">
      <div className="container mx-auto space-y-8">
        <div className="flex justify-between items-center">
          <h1 className="text-4xl font-bold">Web Crawler</h1>
          {isRunning && (
            <div className="flex items-center gap-2">
              <div className="h-3 w-3 rounded-full bg-green-500 animate-pulse" />
              <span className="text-sm text-muted-foreground">Crawling in progress...</span>
            </div>
          )}
        </div>

        <div className="grid gap-8 md:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle>Configuration</CardTitle>
            </CardHeader>
            <CardContent>
              <CrawlConfigForm onSubmit={handleStartCrawl} isRunning={isRunning} />
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Status</CardTitle>
            </CardHeader>
            <CardContent>
              <CrawlStatus isRunning={isRunning} currentUrl={currentUrl} />
            </CardContent>
          </Card>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Recent Content</CardTitle>
          </CardHeader>
          <CardContent>
            <RecentContent />
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
