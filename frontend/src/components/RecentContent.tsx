import { ScrollArea } from "@/components/ui/scroll-area"

interface ProcessedItem {
  url: string
  timestamp: string
  documents: string[]
  status: 'success' | 'error'
}

export function RecentContent() {
  // In a real app, this would be managed by state management like Redux
  // and populated from the API responses
  const recentItems: ProcessedItem[] = []

  return (
    <ScrollArea className="h-[300px] w-full rounded-md border">
      <div className="p-4">
        {recentItems.length === 0 ? (
          <div className="text-center text-sm text-muted-foreground">
            No content processed yet
          </div>
        ) : (
          <div className="space-y-4">
            {recentItems.map((item, index) => (
              <div
                key={index}
                className="rounded-lg border p-4 space-y-2"
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <span className={item.status === 'success' ? "text-green-500" : "text-red-500"}>
                      {item.status === 'success' ? "✅" : "❌"}
                    </span>
                    <a
                      href={item.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-sm font-medium hover:underline break-all"
                    >
                      {item.url}
                    </a>
                  </div>
                  <span className="text-xs text-muted-foreground">
                    {new Date(item.timestamp).toLocaleString()}
                  </span>
                </div>

                {item.documents.length > 0 && (
                  <div className="pl-6 space-y-1">
                    <span className="text-xs font-medium text-muted-foreground">
                      Processed Documents:
                    </span>
                    {item.documents.map((doc, docIndex) => (
                      <div key={docIndex} className="text-xs pl-2">
                        • {doc}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </div>
        )}
      </div>
    </ScrollArea>
  )
}
