import {Navigate} from "react-router";
import GeneratePptPage from "./pages/generate_ppt_page.tsx";
import AboutPage from "./pages/about_page.tsx";

export const routes = [
  {
    path: '',
    element: <Navigate to='/new' />
  },
  {
    path: 'new',
    element: <GeneratePptPage />
  },
  {
    path: 'files',
    element: <div>Hello FILES</div>
  },
  {
    path: 'profile',
    element: <div>Hello PROFILE</div>
  },
  {
    path: 'settings',
    element: <div>Hello SETTINGS</div>
  },
  {
    path: 'about',
    element: <AboutPage />
  },
  {
    path: '*',
    element: <Navigate to='/new' />
  },
]