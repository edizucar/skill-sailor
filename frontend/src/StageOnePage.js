
// Importing modules
import React, { useState, useEffect, useRef } from "react";
import ListElement from "./ListElement";
import "./StageOnePage.css";
import { Box } from "@mui/material";

// material ui stuff



 
function StageOnePage({currentStage, message, changePage, setOption, inputInfo, extractResponse, button1, button2, button3}){

    const selectedOption = () => {
        console.log("init")
    }

    const handleBoxClick = (value)  => {
        return async (event) => {
            setOption(value)
            let m = ""
            if (value == 0) {
                m = button1
            } else if (value == 1) {
                m = button2
            } else {
                m = button3
            }
            await extractResponse(m)
            await changePage()
            
            
        }
    }

    return (
        <div className="StageOnePage">
            <Box  className="StageOneOptions">
                <h2 >{message}</h2>
                <ListElement text={button1} onClick={handleBoxClick(0)}></ListElement>
                <ListElement text={button2} onClick={handleBoxClick(1)}></ListElement>
                <ListElement text={button3} onClick={handleBoxClick(2)}></ListElement>
            </Box>           
        </div>
    );
}

 
export default StageOnePage;