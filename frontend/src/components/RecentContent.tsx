"use client"
import { useEffect, useState } from "react";
import { ScrollArea } from "@/components/ui/scroll-area"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
// import dynamic from 'next/dynamic'
// import lightTheme from '@uiw/react-json-view/light'
// import darkTheme from '@uiw/react-json-view/dark'

// const ReactJson = dynamic(() => import('@uiw/react-json-view'), { ssr: false })

export function RecentContent() {
  const [content, setContent] = useState([]);
  const [metrics, setMetrics] = useState({ status: "idle" });

  useEffect(() => {
    const fetchContent = async () => {
      const response = await fetch("http://localhost:8000/api/crawler/recent");
      if (response.ok) {
        const data = await response.json();
        setContent(data.content);
      }
    };

    const interval = setInterval(fetchContent, 5000); // Fetch status every 5 seconds
    fetchContent(); // Initial fetch

    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    const ws = new WebSocket('ws://localhost:8000/api/crawler/ws/logs')

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      setMetrics(data)
    }

    return () => ws.close()
  }, []);

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle>Recent Content</CardTitle>
      </CardHeader>
      <CardContent>
        <ScrollArea className="h-screen">
          <div className="space-y-2">
            {/* <ReactJson
              value={content}
              style={{ ...lightTheme, padding: '1rem' }}
              displayDataTypes={false}
              collapsed={2}
            /> */}
            <pre>{JSON.stringify(content, null, 2)}</pre>
          </div>
        </ScrollArea>
        <div>
          <h3>Crawl Metrics</h3>
          <pre>{JSON.stringify(metrics, null, 2)}</pre>
        </div>
      </CardContent>
    </Card>
  )
}
