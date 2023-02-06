import React from "react";
import { useParams } from "react-router";
import { ArrowLeftOutlined } from "@ant-design/icons";
import { useNavigate } from "react-router-dom";

import { Space, Button } from "antd";

import AccountTransactions from "../AccountTransactions/AccountTransactions";

const TransactionsPage = () => {
  const { accountId } = useParams();
  const navigate = useNavigate();

  return (
    <Space direction="vertical">
      <Button type="link" onClick={() => navigate(-1)}>
        <ArrowLeftOutlined />
        <span>Back</span>
      </Button>

      <AccountTransactions accountId={accountId} />
    </Space>
  );
};

export default TransactionsPage;
