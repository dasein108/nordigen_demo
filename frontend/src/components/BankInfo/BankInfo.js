import React from "react";

import { Card, Descriptions, List } from "antd";
import { Link } from "react-router-dom";

import { SearchOutlined } from "@ant-design/icons";

const BankAccountDetails = ({ details, account_id }) => {
  const { iban, ...lastData } = details;
  return (
    <Descriptions title={iban}>
      {Object.keys(lastData)
        .filter((k) => ["id", "resourceId"].indexOf(k) === -1)
        .map((k) => (
          <Descriptions.Item key={`desc_${account_id}_${k}`} label={k}>
            {details[k]}
          </Descriptions.Item>
        ))}
    </Descriptions>
  );
};

const BankInfo = ({ data }) => {
  const balances = data.balances.balances
    .filter((b) => b.balanceType === "interimAvailable")
    .map((b) => (
      <div>
        <b>{b.balanceAmount.currency}:</b> {b.balanceAmount.amount}
      </div>
    ));
  return (
    // useEffect(() => loadTodoList(), []);
    <Card
      title={data.name}
      extra={
        <Link to={`transactions/${data.account_id}`}>
          <SearchOutlined /> <span>Transactions</span>
        </Link>
      }
    >
      <BankAccountDetails details={data.details} account_id={data.account_id} />
      <List
        size="small"
        header={<h4>Balances</h4>}
        dataSource={balances}
        renderItem={(item) => <List.Item>{item}</List.Item>}
      />
    </Card>
  );
};

export default BankInfo;
