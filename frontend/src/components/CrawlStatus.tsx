import { Card } from "@/components/ui/card"
import { ScrollArea } from "@/components/ui/scroll-area"

interface CrawlStatusProps {
  isRunning: boolean
  currentUrl: string
}

interface StatusMessage {
  type: 'info' | 'success' | 'error'
  message: string
  timestamp: string
}

export function CrawlStatus({ isRunning, currentUrl }: CrawlStatusProps) {
  return (
    <div className="space-y-4">
      <div className="flex flex-col space-y-2">
        <div className="flex items-center space-x-2">
          <span className="font-medium">Status:</span>
          <span className={isRunning ? "text-green-500" : "text-gray-500"}>
            {isRunning ? "Running" : "Idle"}
          </span>
        </div>
        
        {currentUrl && (
          <div className="flex items-center space-x-2">
            <span className="font-medium">Current URL:</span>
            <span className="text-sm text-muted-foreground break-all">
              {currentUrl}
            </span>
          </div>
        )}
      </div>

      <Card className="p-4">
        <h3 className="font-medium mb-2">Processing Details</h3>
        <ScrollArea className="h-[200px] w-full rounded-md border p-4">
          <div className="space-y-2">
            {currentUrl && (
              <>
                <StatusItem
                  type="info"
                  message={`Started processing ${currentUrl}`}
                />
                {isRunning && (
                  <StatusItem
                    type="info"
                    message="Converting webpage to markdown..."
                  />
                )}
              </>
            )}
          </div>
        </ScrollArea>
      </Card>
    </div>
  )
}

function StatusItem({ type, message }: { type: StatusMessage['type'], message: string }) {
  const colors = {
    info: "text-blue-500",
    success: "text-green-500",
    error: "text-red-500"
  }

  const icons = {
    info: "i️",
    success: "✅",
    error: "❌"
  }

  return (
    <div className="flex items-start space-x-2 text-sm">
      <span>{icons[type]}</span>
      <span className={colors[type]}>{message}</span>
      <span className="text-gray-400 ml-auto">
        {new Date().toLocaleTimeString()}
      </span>
    </div>
  )
}
