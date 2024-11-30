import React, { useState } from "react";
import data from "../idle/note-freq.json";
import ReactPaginate from "react-paginate";

const FreqTable = () => {
  const itemsPerPage = 12;
  const [currentPage, setCurrentPage] = useState(0);

  const handlePageChange = ({ selected }) => {
    setCurrentPage(selected);
  };

  const paginatedData = data.slice(
    currentPage * itemsPerPage,
    (currentPage + 1) * itemsPerPage
  );

  return (
    <div className="max-w-md mx-auto">
      <table className="min-w-full border border-collapse border-gray-800 overflow-hidden">
        <thead>
          <tr>
            <th className="border p-2">Name</th>
            <th className="border p-2">Frequency</th>
          </tr>
        </thead>
        <tbody>
          {paginatedData.map((item, index) => (
            <tr key={index}>
              <td className="border p-2">{item.name}</td>
              <td className="border p-2">{item.freq}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <ReactPaginate
        previousLabel="previous"
        nextLabel="next"
        breakLabel="..."
        pageCount={Math.ceil(data.length / itemsPerPage)}
        marginPagesDisplayed={2}
        pageRangeDisplayed={5}
        onPageChange={handlePageChange}
        containerClassName="flex justify-center mt-4"
        pageLinkClassName="cursor-pointer px-3 py-1 border rounded"
        activeClassName="bg-gray-500 text-white"
      />
    </div>
  );
};

export default FreqTable;