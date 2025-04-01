import { createTheme } from '@mui/material/styles';
import { type Navigation } from '@toolpad/core/AppProvider';
import AutoFixHighIcon from '@mui/icons-material/AutoFixHigh';
import BackupTableIcon from '@mui/icons-material/BackupTable';
import {ReactRouterAppProvider} from "@toolpad/core/react-router";
import {Outlet} from "react-router";

const NAVIGATION: Navigation = [
  {
    segment: 'new',
    title: 'New PPT',
    icon: <AutoFixHighIcon />,
  },
  // {
  //   segment: 'files',
  //   title: 'Files',
  //   icon: <BackupTableIcon />,
  // },
];

const BRANDING = {
  title: 'My Toolpad Core App',
};

const demoTheme = createTheme({
  cssVariables: {
    colorSchemeSelector: 'data-toolpad-color-scheme',
  },
  colorSchemes: { light: true, dark: true },
  breakpoints: {
    values: {
      xs: 0,
      sm: 600,
      md: 600,
      lg: 1200,
      xl: 1536,
    },
  },
});

export default function DashboardLayoutBasic() {
  return (
      <ReactRouterAppProvider
          navigation={NAVIGATION}
          branding={BRANDING}
          theme={demoTheme}
      >
        <Outlet />
      </ReactRouterAppProvider>
  );
}