import {ReactNode, useEffect} from "react";

interface Props {
  children?: ReactNode,
  title: string
}

function Page({children, title}: Props) {

  useEffect(() => {
    document.title = title
  })

  return (
      <>
        {children}
      </>
  );
}

export default Page;