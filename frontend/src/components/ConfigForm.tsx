"use client"
import { useState } from "react";
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Switch } from "@/components/ui/switch"
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"

export function ConfigForm() {
  const [maxDepth, setMaxDepth] = useState(3);
  const [stayOnDomain, setStayOnDomain] = useState(true);
  const [followSubdomains, setFollowSubdomains] = useState(false);
  const [parallelDownloads, setParallelDownloads] = useState(5);
  const [fileTypes, setFileTypes] = useState(".pdf,.doc,.docx,.xls,.xlsx,.csv");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    const response = await fetch("http://localhost:8000/api/crawler/config", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        max_depth: maxDepth,
        stay_on_domain: stayOnDomain,
        follow_subdomains: followSubdomains,
        parallel_downloads: parallelDownloads,
        file_types: fileTypes,
      }),
    });

    if (response.ok) {
      alert("Configuration updated successfully!");
    } else {
      alert("Failed to update configuration.");
    }
  };

  return (
    <Card className="mb-6">
      <CardHeader>
        <CardTitle>Crawler Configuration</CardTitle>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="grid gap-4">
          <div className="space-y-2">
            <Label htmlFor="maxDepth">Max Depth</Label>
            <Input
              id="maxDepth"
              type="number"
              value={maxDepth}
              onChange={(e) => setMaxDepth(Number(e.target.value))}
            />
          </div>
          <div className="flex items-center space-x-2">
            <Switch
              id="stayOnDomain"
              checked={stayOnDomain}
              onCheckedChange={setStayOnDomain}
            />
            <Label htmlFor="stayOnDomain">Stay on Domain</Label>
          </div>
          <div className="flex items-center space-x-2">
            <Switch
              id="followSubdomains"
              checked={followSubdomains}
              onCheckedChange={setFollowSubdomains}
            />
            <Label htmlFor="followSubdomains">Follow Subdomains</Label>
          </div>
          <div className="space-y-2">
            <Label htmlFor="parallelDownloads">Parallel Downloads</Label>
            <Input
              id="parallelDownloads"
              type="number"
              value={parallelDownloads}
              onChange={(e) => setParallelDownloads(Number(e.target.value))}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="fileTypes">File Types</Label>
            <Input
              id="fileTypes"
              value={fileTypes}
              onChange={(e) => setFileTypes(e.target.value)}
            />
          </div>
          <Button type="submit" className="w-full">Update Configuration</Button>
        </form>
      </CardContent>
    </Card>
  )
}
