pragma solidity 0.6.12;

interface PickleJar {
    function balance() external view returns (uint256);

    function available() external view returns (uint256);

    function earn() external;

    function depositAll() external;

    function deposit(uint256 _amount) external;

    function withdrawAll() external;

    function harvest(address reserve, uint256 amount) external;

    function withdraw(uint256 _shares) external;

    function getRatio() external view returns (uint256);

    // from IERC20

    function balanceOf(address) external view returns (uint256);

    function totalSupply() external view returns (uint256);
}
