import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types'
import fetch from 'node-fetch';
import Loader from "react-loader-spinner";

import RouteView from "./RouteView.js";
import UserView from "./UserView.js";
import RouteList from "./RouteList.js";
import Network from "./Network.js"
import './App.css';

function formatRequestUrl(user0, user1) {
    return `http://localhost:5000/api/q=${user0}+${user1}%all`;
}

const initialState = {
    contents: {},
    loaded: false,
    error: false,
}

const APIData = ({ user0, user1 }) => {
    const [state, setState] = useState(initialState);
    user0;
    user1;

    useEffect( () => {
        var requestUrl = formatRequestUrl('200305518', '200696013');
        console.log(requestUrl)

        fetch(requestUrl, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
        })
        .then(r => r.json())
        .then(data => {
            setState({contents: data.all, loaded: true, error: false})
            console.log(data.all)
        })
        .catch((error) => {
            console.error(error);
            setState({contents: {}, loaded: true, error: true})
        });
    }, []);

    return (
        <div className='row'>
            {state.error && ( <>
                <div className="center black-text">
                    Error
                </div>
            </> )}

            {state.loaded ? ( <>
            <div className="row">
                <h4>At a Glance: </h4>
            </div>
            <br></br>
            <div className="row">
                <div className="col s6">
                    <UserView user={state.contents.users[0]} /> 
                </div>
                <div className="col s6">
                    <UserView user={state.contents.users[1]} /> 
                </div>
            </div>

            <div className="row">
                <h5>Tick Network: </h5>
            </div>
            <div className="row">
                <Network graph={state.contents.vis.tick} />
            </div>

            <div className="row">
                <h5>To-do Network: </h5>
            </div>
            <div className="row">
                <Network graph={state.contents.vis.todo} />
            </div>     
            
            <br></br>
            <div className="row">
                <h5>Hardest Climbs: </h5>
            </div>
            <div className="row">
                <h6>Boulder: </h6>
            </div>
            <div className="row">
                <div className="col s6">
                    <RouteView route={state.contents.hardest[0].boulder} /> 
                </div>
                <div className="col s6">
                    <RouteView route={state.contents.hardest[1].boulder} /> 
                </div>
            </div>

            <div className="row">
                <h6>Sport: </h6>
            </div>
            <div className="row">
                <div className="col s6">
                    <RouteView route={state.contents.hardest[0].sport} /> 
                </div>
                <div className="col s6">
                    <RouteView route={state.contents.hardest[1].sport} /> 
                </div>
            </div>

            <div className="row">
                <h6>Trad: </h6>
            </div>
            <div className="row">
                <div className="col s6">
                    <RouteView route={state.contents.hardest[0].trad} /> 
                </div>
                <div className="col s6">
                    <RouteView route={state.contents.hardest[1].trad} /> 
                </div>
            </div>

            <div className="row">
                <h5>Most Popular Climb in Ticks: </h5>
            </div>
            <div className="row">
                <div className="col s6">
                    <RouteView route={state.contents.popular[0]} /> 
                </div>
                <div className="col s6">
                    <RouteView route={state.contents.popular[1]} /> 
                </div>
            </div>

            <div className="row">
                <h5>Least Popular Climb in Ticks: </h5>
            </div>
            <div className="row">
                <div className="col s6">
                    <RouteView route={state.contents.unpopular[0]} /> 
                </div>
                <div className="col s6">
                    <RouteView route={state.contents.unpopular[1]} /> 
                </div>
            </div>

            <div className="row">
                <h5>Ticks in Common: </h5>
            </div>
            <div className="row">
                <RouteList 
                    data={state.contents.tick}
                />
            </div>

            <div className="row">
                <h5>To-dos in Common: </h5>
            </div>
            <div className="row">
                <RouteList 
                    data={state.contents.todo}
                />
            </div>  

            </> ) : ( <>
                <div className="center">
                    <Loader 
                        type="ThreeDots" 
                        color="#000000"
                        height={100}
                        width={100}
                    />
                </div>
            </> )}
        </div>
    );
}

APIData.propTypes = {
    user0: PropTypes.string.isRequired,
    user1: PropTypes.string.isRequired
}

export default APIData;



