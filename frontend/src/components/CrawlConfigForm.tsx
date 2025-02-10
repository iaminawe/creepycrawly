import { useState } from "react"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Switch } from "@/components/ui/switch"
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"

const formSchema = z.object({
  url: z.string().url({ message: "Please enter a valid URL" }),
  s3Bucket: z.string().min(1, { message: "S3 bucket is required" }),
  skipDocs: z.boolean().default(false),
})

interface CrawlConfigFormProps {
  onSubmit: (values: z.infer<typeof formSchema>) => void
  isRunning: boolean
}

export function CrawlConfigForm({ onSubmit, isRunning }: CrawlConfigFormProps) {
  const [error, setError] = useState<string | null>(null)
  
  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      url: "",
      s3Bucket: import.meta.env.VITE_DEFAULT_S3_BUCKET || "",
      skipDocs: false,
    },
  })

  const handleSubmit = async (values: z.infer<typeof formSchema>) => {
    try {
      setError(null)
      
      const response = await fetch("/api/crawl", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          url: values.url,
          s3_bucket: values.s3Bucket,
          skip_docs: values.skipDocs,
        }),
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || "Failed to process webpage")
      }

      const result = await response.json()
      onSubmit(values)
      
      // You could also pass the result to a parent component to display
      // the document URLs that were found and processed
      console.log("Crawl result:", result)
      
    } catch (err) {
      setError(err instanceof Error ? err.message : "An error occurred")
    }
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(handleSubmit)} className="space-y-6">
        <FormField
          control={form.control}
          name="url"
          render={({ field }) => (
            <FormItem>
              <FormLabel>URL</FormLabel>
              <FormControl>
                <Input placeholder="https://example.com" {...field} />
              </FormControl>
              <FormDescription>
                The webpage URL to convert to markdown
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        
        <FormField
          control={form.control}
          name="s3Bucket"
          render={({ field }) => (
            <FormItem>
              <FormLabel>S3 Bucket</FormLabel>
              <FormControl>
                <Input placeholder="my-markdown-bucket" {...field} />
              </FormControl>
              <FormDescription>
                The S3 bucket where markdown files will be stored
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        
        <FormField
          control={form.control}
          name="skipDocs"
          render={({ field }) => (
            <FormItem className="flex flex-row items-center justify-between rounded-lg border p-4">
              <div className="space-y-0.5">
                <FormLabel className="text-base">Skip Documents</FormLabel>
                <FormDescription>
                  Skip processing of linked documents (PDF, Excel, etc.)
                </FormDescription>
              </div>
              <FormControl>
                <Switch
                  checked={field.value}
                  onCheckedChange={field.onChange}
                />
              </FormControl>
            </FormItem>
          )}
        />
        
        {error && (
          <div className="text-sm font-medium text-red-500">
            {error}
          </div>
        )}
        
        <Button type="submit" disabled={isRunning}>
          {isRunning ? "Processing..." : "Start Crawling"}
        </Button>
      </form>
    </Form>
  )
}
