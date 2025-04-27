import time
import logging
import pythoncom
import win32com.client as win32

def create_pptx_from_vba(vba_code, output_path):
    """Injects VBA into PowerPoint, runs the CreatePresentation macro, and saves as macro-enabled PPTM."""
    pythoncom.CoInitializeEx(pythoncom.COINIT_APARTMENTTHREADED)
    powerpoint = None
    presentation = None

    try:
        logging.debug("Launching PowerPoint via DispatchEx")
        powerpoint = win32.DispatchEx("PowerPoint.Application")

        logging.debug("Creating a new presentation")
        presentation = powerpoint.Presentations.Add()

        logging.debug("Injecting VBA module with fixed name")
        vba_module = presentation.VBProject.VBComponents.Add(1)  # vbext_ct_StdModule
        vba_module.Name = "MyModule"
        vba_module.CodeModule.AddFromString(vba_code)

        # Allow macro compilation
        time.sleep(1)
        pythoncom.PumpWaitingMessages()

        logging.debug("Running VBA macro MyModule.MyModule_CreatePresentation")
        powerpoint.Run("MyModule.MyModule_CreatePresentation")

        logging.debug("Saving as PPTM (macro-enabled)")
        presentation.SaveAs(output_path, 25)  # 25 = ppSaveAsOpenXMLPresentationMacroEnabled
        logging.info(f"Saved PPTM to {output_path}")
        return True

    except Exception as e:
        logging.error(f"PPTM Generation Error: {e}")
        return False

    finally:
        if presentation:
            try: presentation.Close()
            except: pass
        if powerpoint:
            try: powerpoint.Quit()
            except: pass
        pythoncom.CoUninitialize()
        time.sleep(1)