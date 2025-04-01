import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import {createBrowserRouter, RouterProvider, Outlet, Navigate} from "react-router";
import { DashboardLayout } from '@toolpad/core/DashboardLayout';
import GeneratePptPage from "./pages/generate_ppt_page.tsx";

function Layout() {
  return (
      <DashboardLayout>
        <div className="p-6">
          <Outlet />
        </div>
      </DashboardLayout>
  );
}

const router = createBrowserRouter([
  {
    element: <App />,
    children: [
      {
        path: '/',
        element: <Layout />,
        children: [
          {
            path: '',
            element: <Navigate to='new' />
          },
          {
            path: 'new',
            element: <GeneratePptPage />
          },
          {
            path: 'files',
            element: <div>Hello FILES</div>
          }
        ]
      },
    ]
  }
]);

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <RouterProvider router={router} />
  </StrictMode>,
)
