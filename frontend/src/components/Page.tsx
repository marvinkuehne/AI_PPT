import {ReactNode, useEffect} from "react";
import {GLOBAL} from "../global_varaibles.ts";

interface Props {
  children?: ReactNode,
  title: string
}

function Page({children, title}: Props) {

  useEffect(() => {
    document.title = GLOBAL.APP_TITLE + ' | ' + title
  })

  return (
      <>
        {children}
      </>
  );
}

export default Page;