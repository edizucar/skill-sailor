// Filename - App.js
 
// Importing modules
import React from "react";
import "./App.css";
import CVPage from "./CVPage";
import StageOnePage from "./StageOnePage";
import { useState } from "react";
import { Box } from "@mui/material";

// importing fonts
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';

// material ui stuff


 
function App() {
    const [stageNum, nextStage] = useState(0);
    const [optionNum, setOption] = useState(0);
    const [profile, setProfile] = useState(null);
    const [button1, setButton1] = useState('');
    const [button2, setButton2] = useState('');
    const [button3, setButton3] = useState('');
    const [stage1Selection, setStage1] = useState('')
    const [stage2Selection, setStage2] = useState('')
    const [stage3Selection, setStage3] = useState('')
    const [finalMsg, setFinal] = useState('')

    // Note state 0 is the CV page
    const incrementStage = () => {
        nextStage(oldStage => oldStage + 1)
    }
    const setProfileWrapper = async (profile) => {
        setProfile(profile);
        await fetch("/stage1", {
            method: 'POST',
            headers: {
                'Content-Type':'application/json'
            },
            body: JSON.stringify(profile)
            }).then((res) =>
            res.json().then((x) => {
                setButton1(x.payload[0]);
                setButton2(x.payload[1]);
                setButton3(x.payload[2]);
            }))
    }

    const setStage1Wrapper = async (message) => {
        setStage1(message)
        await fetch("/stage2", {
            method: 'POST',
            headers: {
                'Content-Type':'application/json'
            },
            body: JSON.stringify({"profile":profile,"message":message})
            }).then((res) =>
            res.json().then((x) => {
                setButton1(x.payload[0]);
                setButton2(x.payload[1]);
                setButton3(x.payload[2]);
            }))
    }
    const setStage2Wrapper = async (message2) => {
        setStage2(message2)
        await fetch("/stage3", {
            method: 'POST',
            headers: {
                'Content-Type':'application/json'
            },
            body: JSON.stringify({"profile":profile,"message1":stage1Selection, "message2":message2})
            }).then((res) =>
            res.json().then((x) => {
                setButton1(x.payload[0]);
                setButton2(x.payload[1]);
                setButton3(x.payload[2]);
            }))
    }

    const setStage3Wrapper = async (message3) => {
        setStage3(message3)
        await fetch("/final", {
            method: 'POST',
            headers: {
                'Content-Type':'application/json'
            },
            body: JSON.stringify({"profile":profile,"message":message3})
            }).then((res) =>
            res.json().then((x) => {
                setFinal(x.payload);
            }))
    }

    return (
        <div className="App">
            {stageNum == 0 && <CVPage changePage={incrementStage} extractResponse={setProfileWrapper}/>}
            {stageNum == 1 && <StageOnePage 
                currentStage={1} 
                message={"Select the sector you would like out of the below options!"} 
                changePage={incrementStage}
                setOption={setOption}
                inputInfo={profile}
                button1={button1}
                button2={button2}
                button3={button3}
                extractResponse={setStage1Wrapper}
            />
            }
            {stageNum == 2 && <StageOnePage 
                currentStage={2} 
                message={"Select the career path you would like out of the below options!"} 
                changePage={incrementStage}
                button1={button1}
                button2={button2}
                button3={button3}
                setOption={setOption}
                extractResponse={setStage2Wrapper}/>
            }
            {stageNum == 3 && <StageOnePage 
                currentStage={3} 
                message={"Select the specialisation you would like out of the below options!"} 
                changePage={incrementStage}
                setOption={setOption}
                button1={button1}
                button2={button2}
                button3={button3}
                extractResponse={setStage3Wrapper}/>
            }
            {stageNum == 4 && 
                <Box className="final">
                    <h1 className="finalTitle">Consider these steps to get started in your career!</h1>
                    <div>{finalMsg}</div>
                </Box>
            }

        </div>
    );
}
 
export default App;