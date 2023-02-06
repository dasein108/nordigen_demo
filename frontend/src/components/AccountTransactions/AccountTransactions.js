import React from "react";

import { Table, Space, Spin } from "antd";

import { useQuery } from "react-query";
import ErrorBox from "../ErrorBox/ErrorBox";
import { fetchTransactions } from "../../services";

const columns = [
  {
    title: "Source",
    dataIndex: "source",
    key: "source",
  },
  {
    title: "Date",
    dataIndex: "valueDate",
    key: "valueDate",
  },
  {
    title: "Info",
    dataIndex: "remittanceInformationUnstructured",
    key: "remittanceInformationUnstructured",
  },
  {
    title: "Amount",
    dataIndex: "transactionAmount",
    key: "transactionAmount",
    render: (transactionAmount) => (
      <div>
        {transactionAmount.amount} &nbsp;
        {transactionAmount.currency}
      </div>
    ),
  },
];

const AccountTransactions = ({ accountId }) => {
  const { data, status, isFetching } = useQuery(
    ["transactions", accountId],
    () => fetchTransactions(accountId)
  );

  return (
    <Space wrap>
      {isFetching && <Spin />}
      {status === "error" && <ErrorBox />}
      {status === "success" && (
        <Table
          columns={columns}
          dataSource={data.data.results}
          rowKey="transactionId"
        />
      )}
    </Space>
  );
};

export default AccountTransactions;
