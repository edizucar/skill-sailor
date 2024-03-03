
// Importing modules
import React, { useState, useEffect } from "react";
import "./CVPage.css";

// material ui stuff
import Button from '@mui/material/Button'
import { TextField } from "@mui/material";
import Box from '@mui/material/Box';
 
function CVPage({changePage, extractResponse}) {
    // useState for setting a javascript
    // object for storing and using data
    const [loading, setLoading] = useState(false);
    const [data, setData] = useState(null);


 

    const [textInput, setTextInput] = useState('hello');

    const handleTextChange = (event) => {
        setTextInput(event.target.value);
      };
    
    const handleButtonClick = async () => {

        setLoading(true)

        // You can perform any action with the textInput state here
        try {
            await fetch("/data", {
                method: 'POST',
                headers: {
                    'Content-Type':'application/json'
                },
                body: JSON.stringify({
                    cv_text:textInput
                })
                }).then((res) =>
                res.json().then((x) => {
                    extractResponse(x)
                })
            );
        } catch (error) {
            console.log(error)
        } finally {
            setLoading(false)
            changePage()
        }
    };
 
    return (
        <div className="CVPage">
            <Box 
                sx={{
                    bgcolor: 'background.paper',
                    display: 'flex',
                    justifyContent: 'center',
                    alignItems: 'center',
                    flexDirection: 'column',
                    minHeight: '100vh',
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
                {!loading &&<Button 
                    sx={{margin:'15px'}}
                    onClick={handleButtonClick} 
                    variant="contained"
                >Submit</Button>}
                {loading && <div className="loader"></div>}
            </Box>

        </div>
    );
}
 
export default CVPage;