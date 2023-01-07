import { Container, Row, Col, Table } from "react-bootstrap"
import '../App.css';
import React, { useState } from 'react'
import axios from 'axios'
import { useInterval } from './utils';



export default function TableData() {
    const [datas, setData] = useState([])
    const [filter, setFilter] = useState('0')
    const [buttonAll, setButtonAll] = useState('push-table-button')
    const [buttonLockToken, setButtonLockToken] = useState('table-button')
    const [buttonStake, setButtonStake] = useState('table-button')

    const url = `http://127.0.0.1:8000/api/?filter=${filter}`

    const getFilterData = () => {
        axios.get(url).then((response) => {
            setData(response.data)
            console.log(datas)
        }
        )
    }
    useInterval(() => {
        getFilterData()
    }, 1000 * 10);

    const filterLockToken = () => {
        setData([])
        setFilter('lockToken')
        setButtonAll('table-button')
        setButtonStake('table-button')
        setButtonLockToken('push-table-button')
    }

    const filterStake = () => {
        setData([])
        setFilter('Stake')
        setButtonAll('table-button')
        setButtonLockToken('table-button')
        setButtonStake('push-table-button')
    }

    const filterReset = () => {
        setData([])
        setFilter('0')
        setButtonAll('push-table-button')
        setButtonStake('table-button')
        setButtonLockToken('table-button')
    }


    return (
        <>  <section>
            <Container>
                <Row>
                    <Col xs={10} md={4} xl={3}>
                        <button onClick={filterReset}>
                            <div className={buttonAll}>
                            <span>All</span>
                        </div>
                        </button>
                        <button className="margin" onClick={filterLockToken}>
                            <div className={buttonLockToken}>
                            <span>Lock Token</span>
                        </div>
                        </button>
                        <button className="margin" onClick={filterStake}>
                            <div className={buttonStake}>
                            <span>Stake</span>
                        </div>
                        </button>
                    </Col>
 
                </Row>
                <Row>
                    <Col xs={12} md={10} xl={10}>
                        <div className="table-bx">
                            <Table responsive>
                                <thead className="th">
                                    <tr>
                                        <th>Txn Hash</th>
                                        <th>Quantity</th>
                                        <th>Method</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {!datas || datas.length <= 0 ? (
                                        <tr>
                                            <td colSpan="3" align="center">
                                                <b>Data loading... Please a wait</b>
                                            </td>
                                        </tr>
                                    ) : (
                                        datas.map(transaction => (
                                            <tr key={transaction.id}>
                                                <td>{transaction.Hash}</td>
                                                <td>{transaction.Amount}</td>
                                                <td>{transaction.Method}</td>
                                            </tr>
                                        ))
                                    )}
                                </tbody>
                            </Table>
                        </div>
                    </Col>
                </Row>
            </Container>
        </section>
        </>
    );
}
