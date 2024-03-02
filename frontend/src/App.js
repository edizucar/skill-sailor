// Filename - App.js
 
// Importing modules
import React, { useState, useEffect } from "react";
import "./App.css";

// importing fonts
import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';

// material ui stuff
import Button from '@mui/material/Button'
import { TextField } from "@mui/material";
import Box from '@mui/material/Box';

 
function App() {
    // useState for setting a javascript
    // object for storing and using data
    const [data, setData] = useState('not got anything');
 

    const [textInput, setTextInput] = useState('hello');

    const handleTextChange = (event) => {
        setTextInput(event.target.value);
      };
    
    const handleButtonClick = () => {
        // Do stuff with the text input
        console.log('Text Input:', textInput);
        // You can perform any action with the textInput state here
        fetch("/data", {
            method: 'POST',
            headers: {
                'Content-Type':'application/json'
            },
            body: JSON.stringify({
                cv_text:textInput
            })
        }).then((res) =>
        res.json().then((x) => {
            setData(JSON.stringify(x))
        })
    );
    };
 
    return (
        <div className="App">
            <Box 
                sx={{
                    bgcolor: 'background.paper',
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                    flexDirection: 'column',
                    height: '100vh',
                    boxShadow: 1,
                    border:3,
                    margin:2,
                    borderRadius: 2,
                    borderColor: 'black',
                    p: 2,
                    minWidth: 300,
                }}
                multiline

            >
                <TextField 
                    sx={{
                        width:'75%',
                    }}
                    id="cv-field" 
                    label="Enter Your CV:"
                    onChange={handleTextChange} 
                    multiline
                />
                <Button 
                    sx={{margin:'15px'}}
                    onClick={handleButtonClick} 
                    variant="contained"
                >Submit</Button>
                <Box>my data is: {data}</Box>
            </Box>

        </div>
    );
}
 
export default App;