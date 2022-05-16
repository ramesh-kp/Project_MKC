import { status } from "@lib/common";
import { render } from "@testing-library/react";
import { ErrorPage } from "./ErrorPage";

const renderErrorPage = (props?: any) => {
  return render(<ErrorPage {...props} />);
};

describe("Error", () => {
  it("error page", () => {
    const { getByTestId } = renderErrorPage();
    expect(getByTestId(status.error)).toHaveTextContent("Error Occured");
  });
});
