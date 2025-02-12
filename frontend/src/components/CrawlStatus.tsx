"use client"
import { useEffect, useState } from "react";
import { ScrollArea } from "@/components/ui/scroll-area"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"

export function CrawlStatus() {
  const [status, setStatus] = useState("");

  useEffect(() => {
    const fetchStatus = async () => {
      const response = await fetch("http://localhost:8000/api/crawler/status");
      if (response.ok) {
        const data = await response.json();
        setStatus(data.status);
      }
    };

    const interval = setInterval(fetchStatus, 5000); // Fetch status every 5 seconds
    fetchStatus(); // Initial fetch

    return () => clearInterval(interval);
  }, []);

  const stopCrawl = async () => {
    try {
      await fetch('http://localhost:8000/api/crawler/stop', { method: 'POST' }); // Correct endpoint
    } catch (error) {
      console.error('Stop failed:', error);
    }
  };

  return (
    <Card className="mb-6">
      <CardHeader>
        <CardTitle>Crawl Status</CardTitle>
      </CardHeader>
      <CardContent>
        <ScrollArea className="h-64">
          <div className="space-y-2">
            <p>{status}</p>
            <button onClick={stopCrawl}>Stop Crawl</button>
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  )
}
