import { createBrowserRouter } from "react-router-dom";
import App from "../App";
import { CrawlConfigForm as CrawlInterface } from "../components/CrawlConfigForm";
import { CrawlStatus as StatusDashboard } from "../components/CrawlStatus";
import { RecentContent as ContentBrowser } from "../components/RecentContent";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      { index: true, element: <CrawlInterface onSubmit={() => {}} isRunning={false} /> },
      { path: "status", element: <StatusDashboard isRunning={false} currentUrl="" /> },
      { path: "content", element: <ContentBrowser /> }
    ]
  }
]);
