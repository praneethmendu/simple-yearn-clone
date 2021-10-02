pragma solidity 0.6.12;

interface PickleFarm {

    function userInfo ( uint256, address ) external view returns ( uint256 amount, int256 rewardDebt );
    
    /// @notice Returns the number of MCV2 pools.
    function poolLength() external view returns (uint256 pools) ;

    /// @notice View function to see pending pickle on frontend.
    /// @param _pid The index of the pool. See `poolInfo`.
    /// @param _user Address of user.
    /// @return pending PICKLE reward for a given user.
    function pendingPickle(uint256 _pid, address _user) external view returns (uint256 pending) ;

    /// @notice Deposit LP tokens to MCV2 for PICKLE allocation.
    /// @param pid The index of the pool. See `poolInfo`.
    /// @param amount LP token amount to deposit.
    /// @param to The receiver of `amount` deposit benefit.
    function deposit(uint256 pid, uint256 amount, address to) external;

    /// @notice Withdraw LP tokens from MCV2.
    /// @param pid The index of the pool. See `poolInfo`.
    /// @param amount LP token amount to withdraw.
    /// @param to Receiver of the LP tokens.
    function withdraw(uint256 pid, uint256 amount, address to) external;

    /// @notice Harvest proceeds for transaction sender to `to`.
    /// @param pid The index of the pool. See `poolInfo`.
    /// @param to Receiver of PICKLE rewards.
    function harvest(uint256 pid, address to) external;
    
    /// @notice Withdraw LP tokens from MCV2 and harvest proceeds for transaction sender to `to`.
    /// @param pid The index of the pool. See `poolInfo`.
    /// @param amount LP token amount to withdraw.
    /// @param to Receiver of the LP tokens and PICKLE rewards.
    function withdrawAndHarvest(uint256 pid, uint256 amount, address to) external;

}