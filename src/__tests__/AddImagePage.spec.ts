import { afterEach, describe, expect, it, vi } from 'vitest'
import { flushPromises, mount } from '@vue/test-utils'
import AddImagePage from '../views/AddImagePage.vue'

vi.mock('@/services/auth', () => ({ getAuthToken: vi.fn().mockResolvedValue('token') }))
afterEach(() => {
  vi.unstubAllGlobals()
  vi.unstubAllEnvs()
})

describe('Add Image', () => {
  async function fillForm() {
    vi.stubEnv('VITE_ADD_IMAGE_API_URL', 'https://api.example.com/gallery')
    const wrapper = mount(AddImagePage, { global: { stubs: { RouterLink: true } } })
    await wrapper.get('#title').setValue('Landscape')
    await wrapper.get('#imageUrl').setValue('https://example.com/art.jpg')
    await wrapper.get('#tags').setValue('nature, mountains, nature')
    return wrapper
  }

  it('sends an authenticated request and clears the form after saving', async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValue({ ok: true, json: async () => ({ status: 'success' }) })
    vi.stubGlobal('fetch', fetchMock)
    const wrapper = await fillForm()
    expect(wrapper.find('input[type="file"]').exists()).toBe(false)
    await wrapper.get('form').trigger('submit')
    await flushPromises()
    const request = fetchMock.mock.calls[0]![1]
    expect(request.headers.Authorization).toBe('Bearer token')
    expect(request.method).toBe('POST')
    expect(JSON.parse(request.body).tags).toEqual(['nature', 'mountains'])
    expect(wrapper.text()).toContain('Your image was added')
    expect((wrapper.get('#title').element as HTMLInputElement).value).toBe('')
  })

  it('preserves input and shows the API error when saving fails', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn().mockResolvedValue({ ok: false, json: async () => ({ message: 'Unable to save.' }) }),
    )
    const wrapper = await fillForm()
    await wrapper.get('form').trigger('submit')
    await flushPromises()
    expect(wrapper.text()).toContain('Unable to save.')
    expect((wrapper.get('#title').element as HTMLInputElement).value).toBe('Landscape')
    expect(wrapper.get('fieldset').attributes('disabled')).toBeUndefined()
  })
})
