import React from "react";

import { Result, Space } from "antd";

const DEFAULT_MESSAGE = "There are some problems with your operation.";

const ErrorBox = ({ title }) => {
  return (
    <Space align="center">
      <Result status="warning" title={title || DEFAULT_MESSAGE} />
    </Space>
  );
};

export default ErrorBox;
