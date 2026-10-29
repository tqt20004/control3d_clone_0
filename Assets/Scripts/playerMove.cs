using Photon.Pun;
using System;
using System.Collections;
using System.Collections.Generic;
using UnityEditor.ShaderGraph.Internal;
using UnityEngine;
using UnityEngine.LowLevel;

public class playerMove : MonoBehaviourPun,IKnockBack
{
    [Header("Góc nhìn & Chuột")]
    public float mouseSensitivity = 100f;
    public Transform playerCamera;
    private float xRotation = 0f;

    Vector3 impactKBackForce;
    PlayerComponent playerComp;

    [Header("Di chuyển & Hoạt ảnh")]
    public float moveSpeed = 6f;
    public Animator animator; // Kéo con 3D Model (F1) vào đây
    private CharacterController controller;
    private Vector3 inputMove;

    public float gravity = -20f;       // Độ mạnh của trọng lực hút xuống đất
    private Vector3 velocityY;         // Biến lưu tốc độ rơi

    void Start()
    {
        playerComp = GetComponent<PlayerComponent>();
        if (animator == null) animator = GetComponentInChildren<Animator>();
        //_______________//
        //AI_CODING
        // NẾU KHÔNG PHẢI LÀ CON CỦA MÌNH (Là con đối thủ):
        // Thêm photonView != null && ở phía trước:
        if (photonView != null && !photonView.IsMine)
        {
            Camera cam = GetComponentInChildren<Camera>();
            if (cam != null) cam.gameObject.SetActive(false);

            AudioListener audio = GetComponentInChildren<AudioListener>();
            if (audio != null) audio.enabled = false;
        }

        // Tự động lấy CharacterController đã gắn trên F0 Player
        controller = GetComponent<CharacterController>();

        // Khóa chuột vào giữa màn hình
        Cursor.lockState = CursorLockMode.Locked;

        
    }
    private void OnEnable()
    {
        SniperGunBehavior.OnScopeChanged += PlayAnimationAiming;
    }
    private void OnDisable()
    {
        SniperGunBehavior.OnScopeChanged -= PlayAnimationAiming;
    }

    void Update()
    {
        if (photonView != null && !photonView.IsMine) return;
        RotatePlayer();
        Move();
        ApplyGravity();
        KnockBack();
    }

    private void ApplyGravity()
    {
        // Nếu chân đã chạm mặt đất thì giữ một lực đè nhẹ -2f để không bị rung chân
        if (controller.isGrounded && velocityY.y < 0)
        {
            velocityY.y = -2f;
        }

        // Tích lũy tốc độ rơi theo thời gian: v = v0 + g * t
        velocityY.y += gravity * Time.deltaTime;

        // Đẩy nhân vật rơi xuống đất theo phương thẳng đứng
        controller.Move(velocityY * Time.deltaTime);
    }
    private void RotatePlayer()
    {
        // 1. Lấy input chuột
        float mouseX = Input.GetAxis("Mouse X") * mouseSensitivity * Time.deltaTime;
        float mouseY = Input.GetAxis("Mouse Y") * mouseSensitivity * Time.deltaTime;

        // Xoay cả người nhân vật theo trục ngang (Trái / Phải)
        transform.Rotate(Vector3.up * mouseX);

        // Xoay riêng Camera theo trục dọc (Lên / Xuống)
        xRotation -= mouseY;
        xRotation = Mathf.Clamp(xRotation, -90f, 90f);

        if (playerCamera != null)
        {
            playerCamera.localRotation = Quaternion.Euler(xRotation, 0f, 0f);
        }
    }

    private void Move()
    {
        inputMove = Vector3.zero;

        // 2. Nhận phím bấm WASD
        if (Input.GetKey(KeyCode.W )) { inputMove += Vector3.forward; }
        if (Input.GetKey(KeyCode.S)) { inputMove += Vector3.back; }
        if (Input.GetKey(KeyCode.A)) { inputMove += Vector3.left; }
        if (Input.GetKey(KeyCode.D)) { inputMove += Vector3.right; }

        // 3. KÍCH HOẠT ANIMATION
        if (animator != null)
        {
            // Nếu có bấm phím (đang di chuyển) -> isRunning = true
            bool isMoving = inputMove.sqrMagnitude > 0.01f;
            animator.SetBool("isRunning", isMoving);
        }

        // 4. Di chuyển nhân vật theo hướng mặt đang nhìn
        inputMove = inputMove.normalized;
        Vector3 dirMove = transform.TransformDirection(inputMove);

        float currentSpeed = moveSpeed; // Giá trị dự phòng mặc định
        if (playerComp != null)
        {
            var moveStat = playerComp.GetStatOfPlayerByCategory(Category_Stats.moveSpeed);
            if (moveStat != null)
            {
                currentSpeed = moveStat.GetValue(); // Lấy tốc độ đã qua tính toán Stun/Slow!
            }
        }

        // Đẩy viên thuốc đi bằng CharacterController
        controller.Move(dirMove * currentSpeed * Time.deltaTime);
    }
    public void PlayAnimationAiming(bool isAiming)
    {
        if (animator == null) return;
            animator.SetBool("isAiming",isAiming);
    }
    public void ExecuteKnockBack(Vector3 dir, float force)
    {
        // Send knockback to the owner of the PhotonView
        if (photonView != null)
        {
            photonView.RPC(nameof(RPC_ApplyKnockBack), photonView.Owner, dir, force);
        }
        else
        {
            // NonNetwork case: Apply knockback alone
            RPC_ApplyKnockBack(dir, force);
        }
    }
    [PunRPC]
    private void RPC_ApplyKnockBack(Vector3 dir, float force)
    {
        impactKBackForce = dir.normalized * force;
        Debug.Log("Máy chủ sở hữu đã nhận lực: " + impactKBackForce);
    }
    public void KnockBack()
    {
        if(impactKBackForce.sqrMagnitude > 0.2f)
        {
            impactKBackForce = Vector3.Lerp(impactKBackForce, Vector3.zero, 2f * Time.deltaTime);
            controller.Move(impactKBackForce * Time.deltaTime);
        }
        else
        {
            impactKBackForce = Vector3.zero;
        }
    }
    
}