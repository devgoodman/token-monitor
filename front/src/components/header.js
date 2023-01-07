import { Container, Row, Col } from "react-bootstrap"

export const Header = () => {
    return (
        <section className="header">
            <Container>
                <Row className="align-items-center">
                    <Col xs={12} md={3} xl={3}>
                        <span className="tagline">Token transaction history</span>
                    </Col>
                </Row>
            </Container>
        </section>
    )
}