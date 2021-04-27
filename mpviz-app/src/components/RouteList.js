import React from 'react';
import PropTypes from 'prop-types'
import { useTable } from "react-table";
import './App.css';

const columns = [
    {
        Header: 'Name',
        accessor: 'name',
    },
    {
        Header: 'Type',
        accessor: 'type',
    },
    {
        Header: 'Grade',
        accessor: 'grade',
    },
    {
        Header: 'Rating',
        accessor: 'rating',
    },
]

const RouteList = ({ data }) => {
    const {
        getTableProps,
        getTableBodyProps,
        headerGroups,
        rows,
        prepareRow,
    } = useTable({
        columns,
        data,
    })
    
      // Render the UI for your table
    return (
        <table {...getTableProps()}>
            <thead>
                {headerGroups.map(headerGroup => (
                    <tr {...headerGroup.getHeaderGroupProps()} key={1}>
                        {headerGroup.headers.map(column => (
                            <th {...column.getHeaderProps()} key={1}>
                                {column.render('Header')}
                            </th>
                        ))}
                    </tr>
                ))}
            </thead>
            <tbody {...getTableBodyProps()}>
                {rows.map((row) => {
                    prepareRow(row)
                    return (
                        <tr {...row.getRowProps()} key={1}>
                            {row.cells.map(cell => {
                                return <td {...cell.getCellProps()} key={1}>
                                    {cell.render('Cell')}
                                </td>
                            })}
                        </tr>
                    )
                })}
            </tbody>
        </table>
    )
}

RouteList.propTypes = {
    data: PropTypes.object.isRequired
}

export default RouteList;