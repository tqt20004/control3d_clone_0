using System;
using UnityEngine;

public class UIManager : MonoBehaviour
{
    public static UIManager Instance { get; private set; }

    [Header("Sniper Scope")]
    [Tooltip("Kéo Image kính ngắm hoặc GameObject Scope vào đây")]
    [SerializeField] private GameObject scopeOverlay;

    private void Awake()
    {
        // Singleton pattern để gọi nhanh bất cứ đâu: UIManager.Instance.ToggleScope(true/false)
        if (Instance == null)
        {
            Instance = this;
        }
        else
        {
            Destroy(gameObject);
            return;
        }

        // Vào game tự động tắt kính ngắm
        if (scopeOverlay != null)
        {
            scopeOverlay.SetActive(false);
        }
    }

    private void OnEnable()
    {
        // Đăng ký lắng nghe sự kiện từ SniperGunBehavior (khi ông thêm event vào)
        SniperGunBehavior.OnScopeChanged += ToggleScope;
    }

    private void OnDisable()
    {
        // Hủy đăng ký để tránh rò rỉ bộ nhớ
        SniperGunBehavior.OnScopeChanged -= ToggleScope;
    }

    /// <summary>
    /// Bật/tắt hiển thị kính ngắm trên màn hình
    /// </summary>
    public void ToggleScope(bool isScoping)
    {
        if (scopeOverlay != null)
        {
            scopeOverlay.SetActive(isScoping);
        }
    }
}
