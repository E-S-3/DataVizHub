import { useEffect } from "react";

const Security = () => {
    useEffect(() => {
        // Handle Keydown Events
        const handleKeyDown = (event) => {
            //  Block Print Screen (PrtScn)
            if (event.key === "PrintScreen") {
                event.preventDefault();
                alert("Screenshots are disabled for security reasons.");
            }

            //  Block Printing (Ctrl + P & Cmd + P for Mac)
            if ((event.ctrlKey || event.metaKey) && event.key === "p") {
                event.preventDefault();
                alert("Printing is disabled for security reasons.");
            }

            //  Block Developer Tools (F12, Ctrl+Shift+I, Ctrl+Shift+J, Ctrl+U)
            if (
                event.key === "F12" || 
                (event.ctrlKey && event.shiftKey && event.key === "I") || 
                (event.ctrlKey && event.shiftKey && event.key === "J") || 
                (event.ctrlKey && event.key === "U") // Block Ctrl+U (View Source)
            ) {
                event.preventDefault();
                alert("Developer tools are disabled for security reasons.");
            }
        };

        //  Disable Right-Click Context Menu
        const disableRightClick = (event) => {
            event.preventDefault();
            alert("Right-click is disabled for security reasons.");
        };

        // Add Event Listeners
        document.addEventListener("contextmenu", disableRightClick);
        document.addEventListener("keydown", handleKeyDown);

        // Cleanup Listeners on Component Unmount
        return () => {
            document.removeEventListener("contextmenu", disableRightClick);
            document.removeEventListener("keydown", handleKeyDown);
        };
    }, []);

    return null; // This component does not render anything
};

export default Security;
