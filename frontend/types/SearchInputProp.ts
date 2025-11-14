import { ChangeEvent } from "react";
export type SearchInputProps = {
  label: string;
  value: string;
  onFocus: () => void;
  onChange: (e: ChangeEvent<HTMLInputElement>) => void;
  placeholder: string;
  children?: React.ReactNode;
};
