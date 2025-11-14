"use client";
import { SearchInputProps } from "@/types/SearchInputProp";
export default function SearchInput({
  label,
  value,
  onFocus,
  onChange,
  placeholder,
}: SearchInputProps) {
  return (
    <div className="relative mb-4">
      <label className="block text-sm font-medium">{label}</label>

      <input
        type="text"
        value={value}
        onFocus={onFocus}
        onChange={(e) => onChange(e)}
        placeholder={placeholder}
        className="mt-1 w-full rounded-lg border-gray-300 shadow-sm focus:ring-2 focus:ring-blue-500 px-3 py-2"
      />
    </div>
  );
}
