import React from 'react'
import {Sigma, RandomizeNodePositions, ForceAtlas2} from 'react-sigma';
import PropTypes from 'prop-types';

import './App.css';

const Network = ({ graph }) => {
    return (
        <>
        <Sigma 
            graph={graph} 
            renderer='canvas'>
            <RandomizeNodePositions/>
            <ForceAtlas2/>
        </Sigma>
        </>
    )
}

Network.propTypes = {
    graph: PropTypes.object.isRequired
}

export default Network;