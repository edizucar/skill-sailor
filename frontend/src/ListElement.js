// Importing modules
import React, { useState, useEffect } from "react";
import "./ListElement.css";

// material ui stuff
import { Box } from "@mui/material";

 
function ListElement({onClick, text}) {

    return (
        <Box className="ListElement" onClick={onClick}>
            {text}
        </Box>
    );
}

 
export default ListElement;