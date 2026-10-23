using UnityEngine;
using Photon.Pun;
using Photon.Realtime;

public class NetworkLauncher : MonoBehaviourPunCallbacks
{
    [Header("Network Settings")]
    [Tooltip("Tên của Prefab Ronaldo trong thư mục Assets/Resources/ (không kèm đuôi .prefab)")]
    [SerializeField] private string playerPrefabName = "Player_Ronaldo";

    [Tooltip("Tên phòng muốn vào")]
    [SerializeField] private string roomName = "SanDau1v1";

    [Tooltip("Số người tối đa trong phòng")]
    [SerializeField] private byte maxPlayers = 2;

    void Start()
    {
        Debug.Log("<color=yellow>[NetworkLauncher] Đang kết nối tới máy chủ Photon Cloud...</color>");
        
        // Đảm bảo khi Host đổi Scene thì các máy khác cũng tự động đổi Scene theo
        PhotonNetwork.AutomaticallySyncScene = true;

        // Bắt đầu kết nối bằng cấu hình trong PhotonServerSettings
        PhotonNetwork.ConnectUsingSettings();
    }

    // Callback khi kết nối thành công tới Master Server
    public override void OnConnectedToMaster()
    {
        Debug.Log("<color=green>[NetworkLauncher] Đã kết nối Master Server thành công! Đang vào phòng: " + roomName + "</color>");

        // Thiết lập cấu hình phòng
        RoomOptions roomOptions = new RoomOptions();
        roomOptions.MaxPlayers = maxPlayers;

        // Tạo hoặc tham gia phòng ngay lập tức (Nếu chưa có thì tự tạo, có rồi thì vào luôn)
        PhotonNetwork.JoinOrCreateRoom(roomName, roomOptions, TypedLobby.Default);
    }

    // Callback khi đã chui vào phòng thành công
    public override void OnJoinedRoom()
    {
        Debug.Log("<color=cyan>[NetworkLauncher] ĐÃ VÀO PHÒNG THÀNH CÔNG! Đang tiến hành spawn nhân vật...</color>");

        // Tạo vị trí ngẫu nhiên một chút để 2 con Ronaldo không bị spawn đè dính chặt vào nhau
        Vector3 randomSpawnPos = new Vector3(Random.Range(-3f, 3f), 1f, Random.Range(-3f, 3f));

        // Bắt buộc Prefab phải nằm trong thư mục: Assets/Resources/
        GameObject player = PhotonNetwork.Instantiate(playerPrefabName, randomSpawnPos, Quaternion.identity);

        if (player != null)
        {
            Debug.Log("<color=green>[NetworkLauncher] Đã spawn thành công nhân vật: " + player.name + "</color>");
        }
    }

    // Callback nếu vào phòng thất bại
    public override void OnJoinRoomFailed(short returnCode, string message)
    {
        Debug.LogError("[NetworkLauncher] Vào phòng thất bại: " + message);
    }

    // Callback khi có người chơi khác bước vào phòng của mình
    public override void OnPlayerEnteredRoom(Player newPlayer)
    {
        Debug.Log("<color=orange>[NetworkLauncher] Người chơi mới đã vào phòng: " + newPlayer.NickName + "</color>");
    }

    // Callback khi đối thủ thoát phòng
    public override void OnPlayerLeftRoom(Player otherPlayer)
    {
        Debug.Log("<color=red>[NetworkLauncher] Đối thủ đã rời phòng: " + otherPlayer.NickName + "</color>");
    }
}
