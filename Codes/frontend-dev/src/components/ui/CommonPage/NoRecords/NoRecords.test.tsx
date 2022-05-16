import React from "react";
import { render } from "@testing-library/react";
import { NoRecords } from "./NoRecords";

const renderNoRecordPage = (props?: any) => {
  return render(<NoRecords {...props} />);
};

describe("Error", () => {
  it("error page", () => {
    const { getByTestId } = renderNoRecordPage();
    expect(getByTestId("norecordsfound")).toHaveTextContent(
      "No Records Found."
    );
  });
});
