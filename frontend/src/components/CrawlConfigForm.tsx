"use client"
import { useState } from "react";
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Switch } from "@/components/ui/switch"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"

export function CrawlConfigForm() {
  const [url, setUrl] = useState("");
  const [s3Bucket, setS3Bucket] = useState("");
  const [skipDocs, setSkipDocs] = useState(false);
  const [downloadFiles, setDownloadFiles] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      setError(null);

      const response = await fetch("http://localhost:8000/api/crawler/crawl", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          url,
          s3_bucket: s3Bucket,
          skip_docs: skipDocs,
          download_files: downloadFiles,
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Failed to process webpage");
      }

      const result = await response.json();
      alert("Crawling started successfully!");
      console.log("Crawl result:", result);

    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred");
    }
  };

  return (
    <Card className="mb-6">
      <CardHeader>
        <CardTitle>New Web Crawl</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="grid gap-4">
          <div className="space-y-2">
            <Label htmlFor="url">Website URL</Label>
            <Input
              id="url"
              placeholder="https://example.com"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="s3Bucket">S3 Bucket</Label>
            <Input
              id="s3Bucket"
              placeholder="my-markdown-bucket"
              value={s3Bucket}
              onChange={(e) => setS3Bucket(e.target.value)}
            />
          </div>
          <div className="flex items-center space-x-2">
            <Switch
              id="skipDocs"
              checked={skipDocs}
              onCheckedChange={setSkipDocs}
            />
            <Label htmlFor="skipDocs">Skip Documents</Label>
          </div>
          <div className="flex items-center space-x-2">
            <Switch
              id="downloadFiles"
              checked={downloadFiles}
              onCheckedChange={setDownloadFiles}
            />
            <Label htmlFor="downloadFiles">Download Files</Label>
          </div>
          {error && (
            <div className="text-sm font-medium text-red-500">
              {error}
            </div>
          )}
          <Button type="submit" className="w-full">Start Crawling</Button>
        </form>
      </CardContent>
    </Card>
  )
}
